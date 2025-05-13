from django.shortcuts import render
from django.contrib.auth.decorators import login_required


# Create your views here.
@login_required
def home(request):
    return render(request,"dashboard.html")


def login(request):
    return render(request,"login.html")










import json
import paypalrestsdk
from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST, require_GET
from django.conf import settings
from django.contrib.auth.decorators import login_required
from .models import Subscription
# from .paypal_config import configure_paypal # Ensure SDK is configured

# Ensure PayPal SDK is configured (redundant if done in apps.py ready())
# configure_paypal()

@login_required
@require_GET
def subscribe_view(request):
    """Displays the subscription page with the PayPal button."""
    user = request.user

    # Fetch or determine PayPal plan IDs (you can also hardcode if fixed)
    #plan_ids = get_or_create_billing_plans()  # returns a dict like {'basic': '...', 'pro': '...', 'unlimited': '...'}
    
    # Check if user has an active subscription
    active_subscription = Subscription.objects.filter(user=user, status='ACTIVE').first()

    context = {
        'active_subscription': active_subscription,
        'basic_plan_id': settings.PAYPAL_PLAN_ID_BASIC,#plan_ids['basic'],
        'pro_plan_id': settings.PAYPAL_PLAN_ID_STANDARD,#plan_ids['pro'],
        'unlimited_plan_id': settings.PAYPAL_PLAN_ID_PREMIUM,#plan_ids['unlimited'],
        'paypal_client_id': settings.PAYPAL_CLIENT_ID,
    }
    # context = {
    #     'paypal_client_id': settings.PAYPAL_CLIENT_ID,
    #     'paypal_plan_id': settings.PAYPAL_PLAN_ID,
    # }
    return render(request, 'subscriptions/dashboard.html', context)

@login_required
@require_POST
@csrf_exempt # Temporarily exempt for fetch POST, ensure CSRF passed in header
def save_subscription_view(request):
    """Saves the subscription details after successful PayPal approval."""
    if not request.user.is_authenticated:
         return JsonResponse({'error': 'User not authenticated'}, status=403)

    try:
        data = json.loads(request.body)
        paypal_subscription_id = data.get('subscriptionID')
        paypal_plan_id = data.get('planID') # Get plan ID from request

        if not paypal_subscription_id or not paypal_plan_id:
            return JsonResponse({'error': 'Missing subscriptionID or planID'}, status=400)

        # Optional: Verify subscription details with PayPal API (recommended)
        # try:
        #     sub = paypalrestsdk.Subscription.find(paypal_subscription_id)
        #     if not sub or sub.plan_id != paypal_plan_id: # Basic validation
        #          raise ValueError("Subscription details mismatch or not found")
        #     paypal_status = sub.status # e.g., 'ACTIVE'
        # except paypalrestsdk.ResourceNotFound:
        #      return JsonResponse({'error': 'PayPal Subscription not found'}, status=404)
        # except Exception as e:
        #      print(f"Error verifying PayPal subscription {paypal_subscription_id}: {e}")
        #      return JsonResponse({'error': 'Could not verify subscription with PayPal'}, status=500)


        # Check if this subscription ID already exists for this user or another user
        if Subscription.objects.filter(paypal_subscription_id=paypal_subscription_id).exists():
             return JsonResponse({'error': 'Subscription already processed'}, status=400)

        # Create or update the subscription record in your database
        subscription, created = Subscription.objects.update_or_create(
            user=request.user,
            paypal_plan_id=paypal_plan_id, # Store the plan ID
            defaults={
                'paypal_subscription_id': paypal_subscription_id,
                'status': 'PENDING', # Initially set to PENDING or ACTIVE if verified
                # 'status': paypal_status if verified, else 'PENDING',
            }
        )

        print(f"Subscription {'created' if created else 'updated'} for user {request.user.username}: ID {subscription.id}, PayPal ID {paypal_subscription_id}")

        # Important: The subscription might not be instantly 'ACTIVE'.
        # Rely on Webhooks (Phase 6) to confirm activation and ongoing payments.

        return JsonResponse({'success': True, 'subscription_id': subscription.id})

    except json.JSONDecodeError:
        return JsonResponse({'success': False,'error': 'Invalid JSON'}, status=400)
    except Exception as e:
        print(f"Error saving subscription: {e}")
        # Log the error details here
        return JsonResponse({'success': False,'error': 'An internal server error occurred.'}, status=500)


@login_required
@require_GET
def subscription_success_view(request):
    """Page shown after successfully initiating the subscription save."""
    # You might want to fetch the latest subscription status here or just show a generic message
    try:
        latest_subscription = Subscription.objects.filter(user=request.user).latest('created_at')
        context = {'subscription': latest_subscription}
    except Subscription.DoesNotExist:
        context = {'subscription': None} # Should not happen if redirected correctly
    return render(request, 'subscriptions/subscription_success.html', context)

@login_required
@require_GET
def subscription_cancel_view(request):
    """Page shown if the user cancels the PayPal flow."""
    #return render(request, 'subscriptions/subscription_cancel.html')

    sub = Subscription.objects.filter(user=request.user, status='ACTIVE').first()
    if sub:
        sub.status = 'CANCELLED'
        sub.save()
    return JsonResponse({"success": True})


@csrf_exempt
@login_required
def update_subscription_plan(request):
    import os
    import requests
    data = json.loads(request.body)
    subscription_id = data.get("subscription_id")
    new_plan_id = data.get("new_plan_id")

    client_id = os.environ['PAYPAL_CLIENT_ID']
    client_secret = os.environ['PAYPAL_CLIENT_SECRET']

    auth_response = requests.post(
        'https://api-m.sandbox.paypal.com/v1/oauth2/token',
        auth=(client_id, client_secret),
        headers={'Accept': 'application/json'},
        data={'grant_type': 'client_credentials'}
    )
    if auth_response.status_code != 200:
        return JsonResponse({"success": False, "error": "PayPal Auth Failed"})

    access_token = auth_response.json()['access_token']

    patch_data = [{
        "op": "replace",
        "path": "/plan_id",
        "value": new_plan_id
    }]

    patch_response = requests.patch(
        f"https://api-m.sandbox.paypal.com/v1/billing/subscriptions/{subscription_id}",
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {access_token}"
        },
        json=patch_data
    )

    if patch_response.status_code == 204:
        # Update local DB
        Subscription.objects.filter(paypal_subscription_id=subscription_id).update(
            paypal_plan_id=new_plan_id
        )
        return JsonResponse({"success": True})
    else:
        return JsonResponse({
            "success": False,
            "error": patch_response.json().get("message", "Unknown error")
        })


# --- Webhook Handler ---

@csrf_exempt # PayPal POST requests won't have Django CSRF token
@require_POST
def paypal_webhook_view(request):
    """Handles incoming webhooks from PayPal."""
    # 1. Verify the Webhook Signature (CRITICAL FOR SECURITY)
    transmission_id = request.headers.get('Paypal-Transmission-Id')
    timestamp = request.headers.get('Paypal-Transmission-Time')
    webhook_id = settings.PAYPAL_WEBHOOK_ID # Get your Webhook ID from PayPal dashboard & settings
    event_body = request.body.decode(request.encoding or 'utf-8')
    cert_url = request.headers.get('Paypal-Cert-Url')
    auth_algo = request.headers.get('Paypal-Auth-Algo')
    actual_sig = request.headers.get('Paypal-Transmission-Sig')

    if not all([transmission_id, timestamp, webhook_id, event_body, cert_url, auth_algo, actual_sig]):
         print("Webhook Error: Missing headers.")
         return HttpResponseBadRequest("Missing required PayPal headers.")

    try:
        # This uses the SDK's verification method
        event_verified = paypalrestsdk.WebhookEvent.verify(
            transmission_id=transmission_id,
            timestamp=timestamp,
            webhook_id=webhook_id,
            event_body=event_body,
            cert_url=cert_url,
            auth_algo=auth_algo,
            actual_sig=actual_sig
        )
    except Exception as e:
        print(f"Webhook verification error: {e}")
        return HttpResponseForbidden("Webhook verification failed.")

    if not event_verified:
        print("Webhook Error: Signature verification failed.")
        return HttpResponseForbidden("Webhook signature verification failed.")

    # 2. Process the Verified Event
    try:
        event_data = json.loads(event_body)
        event_type = event_data.get('event_type')
        resource = event_data.get('resource', {})
        subscription_id = resource.get('id') or resource.get('billing_agreement_id') # ID might be in different places

        print(f"Received verified PayPal webhook. Event: {event_type}, Subscription ID: {subscription_id}")

        if not subscription_id:
             print("Webhook Info: No subscription ID found in resource.")
             # Could be a different type of event, log or ignore if not relevant
             return HttpResponse("Webhook received, but no relevant subscription ID found.")

        # Find the local subscription record
        try:
            local_subscription = Subscription.objects.get(paypal_subscription_id=subscription_id)
        except Subscription.DoesNotExist:
            print(f"Webhook Warning: Received event for unknown subscription ID: {subscription_id}")
            # Decide how to handle this - maybe log and ignore, or create a record if appropriate?
            # For now, we'll ignore events for unknown subs.
            return HttpResponse("Webhook received for unknown subscription.")

        # Update local subscription status based on event type
        # See PayPal docs for all event types: https://developer.paypal.com/docs/api/webhooks/v1/#event-type
        if event_type == 'BILLING.SUBSCRIPTION.ACTIVATED':
            local_subscription.status = 'ACTIVE'
            # You might want to fetch billing_info for start/next billing date here
            # sub_details = paypalrestsdk.Subscription.find(subscription_id)
            # local_subscription.start_date = sub_details.start_time # Adjust parsing as needed
            # local_subscription.next_billing_date = sub_details.billing_info.next_billing_time
            print(f"Activated subscription {subscription_id} for user {local_subscription.user.username}")

        elif event_type == 'BILLING.SUBSCRIPTION.CANCELLED':
            local_subscription.status = 'CANCELLED'
            print(f"Cancelled subscription {subscription_id} for user {local_subscription.user.username}")

        elif event_type == 'BILLING.SUBSCRIPTION.EXPIRED':
            local_subscription.status = 'EXPIRED'
            print(f"Expired subscription {subscription_id} for user {local_subscription.user.username}")

        elif event_type == 'BILLING.SUBSCRIPTION.SUSPENDED':
            local_subscription.status = 'SUSPENDED'
            print(f"Suspended subscription {subscription_id} for user {local_subscription.user.username}")

        elif event_type == 'BILLING.SUBSCRIPTION.UPDATED':
            # Plan changed, price changed, etc. You might want to fetch details.
            print(f"Updated subscription {subscription_id} for user {local_subscription.user.username}")
            # sub_details = paypalrestsdk.Subscription.find(subscription_id) # Fetch new details if needed
            pass # Update local fields if necessary

        elif event_type == 'PAYMENT.SALE.COMPLETED':
            # This confirms a recurring payment was successful
            # You might update the `next_billing_date` based on this.
            # billing_agreement_id = resource.get('billing_agreement_id')
            # Find subscription by billing_agreement_id if different from resource id
            print(f"Payment received for subscription {subscription_id}")
            # Fetch subscription details to get next billing date if needed
            # sub_details = paypalrestsdk.Subscription.find(subscription_id)
            # local_subscription.next_billing_date = sub_details.billing_info.next_billing_time

        # Add other event types as needed (e.g., PAYMENT.SALE.DENIED, BILLING.SUBSCRIPTION.PAYMENT.FAILED)

        local_subscription.save()

        # 3. Return 200 OK to PayPal
        return HttpResponse("Webhook received and processed.", status=200)

    except json.JSONDecodeError:
        print("Webhook Error: Invalid JSON received.")
        return HttpResponseBadRequest("Invalid JSON payload.")
    except Exception as e:
        print(f"Webhook Error: Internal server error processing event: {e}")
        # Log the full error traceback here
        return HttpResponse("Internal server error processing webhook.", status=500)