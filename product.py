import requests

headers = {
    'Authorization': 'Bearer A21AAKNVF9cvuhVZFGzX8FncIs1GnmTp2fqgBn029n7BH9_3wroR8qqtAzAyOwSu85LeRrNPDr8YgigbX0c2VtIZmTVPGa7Rw',
    'Content-Type': 'application/json',
    'Accept': 'application/json',
    # 'PayPal-Request-Id': 'PRODUCT-18062019-001',
    'Prefer': 'return=representation',
}

data = '{ "name": "ViralSort", "description": "Instagram Reel Sorting service", "type": "SERVICE", "category": "SOFTWARE"}'

response = requests.post('https://api-m.sandbox.paypal.com/v1/catalogs/products', headers=headers, data=data)


print(response.json())


{'id': 'PROD-65R61616853458744', 'name': 'ViralSort', 'description': 'Instagram Reel Sorting service', 'type': 'SERVICE', 'category': 'SOFTWARE', 'create_time': '2025-05-10T08:37:20Z', 'update_time': '2025-05-10T08:37:20Z', 'links': [{'href': 'https://api.sandbox.paypal.com/v1/catalogs/products/PROD-65R61616853458744', 'rel': 'self', 'method': 'GET'}, {'href': 'https://api.sandbox.paypal.com/v1/catalogs/products/PROD-65R61616853458744', 'rel': 'edit', 'method': 'PATCH'}]} 


# import requests
# from requests.auth import HTTPBasicAuth

# # Replace these with your actual PayPal sandbox credentials
# CLIENT_ID = 'Ae_wHvG4kVcVcG0hTsaKHGsm4Li6tjbZX3SPv-09BJbQ2-CgYl48bKn_ow8U0bZezX6JH6Ji8Qia2W_6'
# CLIENT_SECRET = 'ECfyfWNcawsouzPiYXgUiNxpgTL2pfIAq1rlrxNUGe9D54-pINDt4aNt3JPys1QqjSg37B4VNHk8bnGK'

# url = "https://api-m.sandbox.paypal.com/v1/oauth2/token"

# headers = {
#     "Content-Type": "application/x-www-form-urlencoded"
# }

# data = {
#     "grant_type": "client_credentials"
# }

# response = requests.post(
#     url,
#     headers=headers,
#     data=data,
#     auth=HTTPBasicAuth(CLIENT_ID, CLIENT_SECRET)
# )

# print(response.status_code)
# print(response.json())

# {'scope': 'https://uri.paypal.com/services/checkout/one-click-with-merchant-issued-token https://uri.paypal.com/services/payments/futurepayments https://uri.paypal.com/services/invoicing https://uri.paypal.com/services/vault/payment-tokens/read https://uri.paypal.com/services/disputes/read-buyer https://uri.paypal.com/services/payments/realtimepayment https://api.paypal.com/v1/vault/credit-card https://api.paypal.com/v1/payments/.* https://uri.paypal.com/services/vault/payment-tokens/readwrite https://uri.paypal.com/services/applications/webhooks https://uri.paypal.com/services/pricing/exchange-currency/read https://uri.paypal.com/services/disputes/update-seller https://uri.paypal.com/services/payments/payment/authcapture openid https://uri.paypal.com/services/disputes/read-seller Braintree:Vault https://uri.paypal.com/services/payments/refund https://uri.paypal.com/services/documents/disputes/download https://uri.paypal.com/services/pricing/quote-exchange-rates/read https://uri.paypal.com/services/billing-agreements https://uri.paypal.com/payments/payouts https://api.paypal.com/v1/vault/credit-card/.* https://uri.paypal.com/services/shipping/trackers/readwrite https://uri.paypal.com/services/subscriptions', 'access_token': 'A21AAKNVF9cvuhVZFGzX8FncIs1GnmTp2fqgBn029n7BH9_3wroR8qqtAzAyOwSu85LeRrNPDr8YgigbX0c2VtIZmTVPGa7Rw', 'token_type': 'Bearer', 'app_id': 'APP-80W284485P519543T', 'expires_in': 32400, 'nonce': '2025-05-10T08:36:04ZHm6OypNgKQxHtG_7jWz30JkEBFyRg8NAaVM_RDEsh_U'}




# {'scope': 'https://uri.paypal.com/services/checkout/one-click-with-merchant-issued-token https://uri.paypal.com/services/payments/futurepayments https://uri.paypal.com/services/invoicing https://uri.paypal.com/services/vault/payment-tokens/read https://uri.paypal.com/services/disputes/read-buyer https://uri.paypal.com/services/payments/realtimepayment https://api.paypal.com/v1/vault/credit-card https://api.paypal.com/v1/payments/.* https://uri.paypal.com/services/vault/payment-tokens/readwrite https://uri.paypal.com/services/applications/webhooks https://uri.paypal.com/services/pricing/exchange-currency/read https://uri.paypal.com/services/disputes/update-seller https://uri.paypal.com/services/payments/payment/authcapture openid https://uri.paypal.com/services/disputes/read-seller Braintree:Vault https://uri.paypal.com/services/payments/refund https://uri.paypal.com/services/documents/disputes/download https://uri.paypal.com/services/pricing/quote-exchange-rates/read https://uri.paypal.com/services/billing-agreements https://uri.paypal.com/payments/payouts https://api.paypal.com/v1/vault/credit-card/.* https://uri.paypal.com/services/shipping/trackers/readwrite https://uri.paypal.com/services/subscriptions', 'access_token': 'A21AAI7SpkRq4H4tBFUnZ-x7hAjIPArsdWQZpx7chrZOV3cbXoMoYrR3rjtsEO2enC4pLI650mmQQBP4owKj9ApNMvOLLAoWQ', 'token_type': 'Bearer', 'app_id': 'APP-80W284485P519543T', 'expires_in': 32400, 'nonce': '2025-05-13T11:42:13ZXTwYAPTsx7rb2RJ_R0uQDEdvbSua23TeBdRNVsiHqMo'}