# subscriptions/utils.py (or a suitable place)
import requests
import time
from django.conf import settings
# import logging # Use Django's logging

# logger = logging.getLogger(__name__)

# Basic in-memory cache for access token
_paypal_access_token_cache = {
    "token": None,
    "expires_at": 0,
}

def get_paypal_access_token():
    """
    Retrieves a PayPal OAuth2 access token, caching it in memory.
    """
    global _paypal_access_token_cache
    current_time = time.time()

    # Return cached token if it's still valid (with a 60-second buffer)
    if _paypal_access_token_cache["token"] and current_time < (_paypal_access_token_cache["expires_at"] - 60):
        return _paypal_access_token_cache["token"]

    auth_url = f"{settings.PAYPAL_API_BASE_URL}/v1/oauth2/token"
    headers = {
        "Accept": "application/json",
        "Accept-Language": "en_US",
    }
    data = {
        "grant_type": "client_credentials",
    }

    try:
        response = requests.post(
            auth_url,
            auth=(settings.PAYPAL_CLIENT_ID, settings.PAYPAL_CLIENT_SECRET),
            headers=headers,
            data=data,
        )
        response.raise_for_status()  # Raises HTTPError for bad responses (4XX or 5XX)
        token_data = response.json()

        _paypal_access_token_cache["token"] = token_data["access_token"]
        _paypal_access_token_cache["expires_at"] = current_time + token_data["expires_in"]
        #logger.info("Successfully obtained new PayPal access token.")
        return _paypal_access_token_cache["token"]
    except requests.exceptions.RequestException as e:
        #logger.error(f"Error obtaining PayPal access token: {e}")
        #logger.error(f"Response content: {e.response.content if e.response else 'No response'}")
        return None
    except KeyError:
        #logger.error("Access token or expires_in not found in PayPal's token response.")
        return None