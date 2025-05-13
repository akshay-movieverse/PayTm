# import requests

# headers = {
#     'Authorization': 'Bearer A21AAKNVF9cvuhVZFGzX8FncIs1GnmTp2fqgBn029n7BH9_3wroR8qqtAzAyOwSu85LeRrNPDr8YgigbX0c2VtIZmTVPGa7Rw',
#     'Content-Type': 'application/json',
#     'Accept': 'application/json',
#     # 'PayPal-Request-Id': 'PLAN-18062019-001',
#     'Prefer': 'return=representation',
# }

# data = '{ "product_id": "PROD-65R61616853458744", "name": "ViralSort Service Plan", "description": "ViralSort Service basic plan", "status": "ACTIVE", "billing_cycles": [ { "frequency": { "interval_unit": "MONTH", "interval_count": 1 }, "tenure_type": "TRIAL", "sequence": 1, "total_cycles": 2, "pricing_scheme": { "fixed_price": { "value": "3", "currency_code": "USD" } } }, { "frequency": { "interval_unit": "MONTH", "interval_count": 1 }, "tenure_type": "TRIAL", "sequence": 2, "total_cycles": 3, "pricing_scheme": { "fixed_price": { "value": "6", "currency_code": "USD" } } }, { "frequency": { "interval_unit": "MONTH", "interval_count": 1 }, "tenure_type": "REGULAR", "sequence": 3, "total_cycles": 12, "pricing_scheme": { "fixed_price": { "value": "10", "currency_code": "USD" } } } ], "payment_preferences": { "auto_bill_outstanding": true, "setup_fee": { "value": "10", "currency_code": "USD" }, "setup_fee_failure_action": "CONTINUE", "payment_failure_threshold": 3 }, "taxes": { "percentage": "10", "inclusive": false } }'

# response = requests.post('https://api-m.sandbox.paypal.com/v1/billing/plans', headers=headers, data=data)

# print(response.json())


# {'id': 'P-6GP7250575551542BNAPREEI', 'product_id': 'PROD-65R61616853458744', 'name': 'ViralSort Service Plan', 'status': 'ACTIVE', 'description': 'ViralSort Service basic plan', 'usage_type': 'LICENSED', 'billing_cycles': [{'pricing_scheme': {'version': 1, 'fixed_price': {'currency_code': 'USD', 'value': '3.0'}, 'create_time': '2025-05-10T08:45:05Z', 'update_time': '2025-05-10T08:45:05Z'}, 'frequency': {'interval_unit': 'MONTH', 'interval_count': 1}, 'tenure_type': 'TRIAL', 'sequence': 1, 'total_cycles': 2}, {'pricing_scheme': {'version': 1, 'fixed_price': {'currency_code': 'USD', 'value': '6.0'}, 'create_time': '2025-05-10T08:45:05Z', 'update_time': '2025-05-10T08:45:05Z'}, 'frequency': {'interval_unit': 'MONTH', 'interval_count': 1}, 'tenure_type': 'TRIAL', 'sequence': 2, 'total_cycles': 3}, {'pricing_scheme': {'version': 1, 'fixed_price': {'currency_code': 'USD', 'value': '10.0'}, 'create_time': '2025-05-10T08:45:05Z', 'update_time': '2025-05-10T08:45:05Z'}, 'frequency': {'interval_unit': 'MONTH', 'interval_count': 1}, 'tenure_type': 'REGULAR', 'sequence': 3, 'total_cycles': 12}], 'payment_preferences': {'service_type': 'PREPAID', 'auto_bill_outstanding': True, 'setup_fee': {'currency_code': 'USD', 'value': '10.0'}, 'setup_fee_failure_action': 'CONTINUE', 'payment_failure_threshold': 3}, 'taxes': {'percentage': '10.0', 'inclusive': False}, 'quantity_supported': False, 'create_time': '2025-05-10T08:45:05Z', 'update_time': '2025-05-10T08:45:05Z', 'links': [{'href': 'https://api.sandbox.paypal.com/v1/billing/plans/P-6GP7250575551542BNAPREEI', 'rel': 'self', 'method': 'GET', 'encType': 'application/json'}, {'href': 'https://api.sandbox.paypal.com/v1/billing/plans/P-6GP7250575551542BNAPREEI', 'rel': 'edit', 'method': 'PATCH', 'encType': 'application/json'}, {'href': 'https://api.sandbox.paypal.com/v1/billing/plans/P-6GP7250575551542BNAPREEI/deactivate', 'rel': 'self', 'method': 'POST', 'encType': 'application/json'}]}




import requests
import json

headers = {
    'Authorization': 'Bearer A21AAI7SpkRq4H4tBFUnZ-x7hAjIPArsdWQZpx7chrZOV3cbXoMoYrR3rjtsEO2enC4pLI650mmQQBP4owKj9ApNMvOLLAoWQ',
    'Content-Type': 'application/json',
    'Accept': 'application/json',
    'Prefer': 'return=representation',
}

data = {
    "product_id": "PROD-65R61616853458744",  # Replace with your actual Product ID
    "name": "Unlimited Monthly Plan",
    "description": "A simple subscription for $5/month",
    "status": "ACTIVE",
    "billing_cycles": [
        {
            "frequency": {
                "interval_unit": "MONTH",
                "interval_count": 1
            },
            "tenure_type": "REGULAR",
            "sequence": 1,
            "total_cycles": 0,  # 0 = infinite until user cancels
            "pricing_scheme": {
                "fixed_price": {
                    "value": "20",
                    "currency_code": "USD"
                }
            }
        }
    ],
    "payment_preferences": {
        "auto_bill_outstanding": True,
        "setup_fee_failure_action": "CONTINUE",
        "payment_failure_threshold": 3
    }
}

response = requests.post(
    'https://api-m.sandbox.paypal.com/v1/billing/plans',
    headers=headers,
    data=json.dumps(data)  # Proper JSON encoding
)

print(response.status_code)
print(response.json())


#5$ {'id': 'P-71421155EJ7230933NARTARQ', 'product_id': 'PROD-65R61616853458744', 'name': 'Simple Monthly Plan', 'status': 'ACTIVE', 'description': 'A simple subscription for $5/month', 'usage_type': 'LICENSED', 'billing_cycles': [{'pricing_scheme': {'version': 1, 'fixed_price': {'currency_code': 'USD', 'value': '5.0'}, 'create_time': '2025-05-13T11:43:02Z', 'update_time': '2025-05-13T11:43:02Z'}, 'frequency': {'interval_unit': 'MONTH', 'interval_count': 1}, 'tenure_type': 'REGULAR', 'sequence': 1, 'total_cycles': 0}], 'payment_preferences': {'service_type': 'PREPAID', 'auto_bill_outstanding': True, 'setup_fee': {'currency_code': 'USD', 'value': '0.0'}, 'setup_fee_failure_action': 'CONTINUE', 'payment_failure_threshold': 3}, 'quantity_supported': False, 'create_time': '2025-05-13T11:43:02Z', 'update_time': '2025-05-13T11:43:02Z', 'links': [{'href': 'https://api.sandbox.paypal.com/v1/billing/plans/P-71421155EJ7230933NARTARQ', 'rel': 'self', 'method': 'GET', 'encType': 'application/json'}, {'href': 'https://api.sandbox.paypal.com/v1/billing/plans/P-71421155EJ7230933NARTARQ', 'rel': 'edit', 'method': 'PATCH', 'encType': 'application/json'}, {'href': 'https://api.sandbox.paypal.com/v1/billing/plans/P-71421155EJ7230933NARTARQ/deactivate', 'rel': 'self', 'method': 'POST', 'encType': 'application/json'}]}

#10$ {'id': 'P-1X373873NY326071TNARTBFY', 'product_id': 'PROD-65R61616853458744', 'name': 'Pro Monthly Plan', 'status': 'ACTIVE', 'description': 'A simple subscription for $5/month', 'usage_type': 'LICENSED', 'billing_cycles': [{'pricing_scheme': {'version': 1, 'fixed_price': {'currency_code': 'USD', 'value': '10.0'}, 'create_time': '2025-05-13T11:44:23Z', 'update_time': '2025-05-13T11:44:23Z'}, 'frequency': {'interval_unit': 'MONTH', 'interval_count': 1}, 'tenure_type': 'REGULAR', 'sequence': 1, 'total_cycles': 0}], 'payment_preferences': {'service_type': 'PREPAID', 'auto_bill_outstanding': True, 'setup_fee': {'currency_code': 'USD', 'value': '0.0'}, 'setup_fee_failure_action': 'CONTINUE', 'payment_failure_threshold': 3}, 'quantity_supported': False, 'create_time': '2025-05-13T11:44:23Z', 'update_time': '2025-05-13T11:44:23Z', 'links': [{'href': 'https://api.sandbox.paypal.com/v1/billing/plans/P-1X373873NY326071TNARTBFY', 'rel': 'self', 'method': 'GET', 'encType': 'application/json'}, {'href': 'https://api.sandbox.paypal.com/v1/billing/plans/P-1X373873NY326071TNARTBFY', 'rel': 'edit', 'method': 'PATCH', 'encType': 'application/json'}, {'href': 'https://api.sandbox.paypal.com/v1/billing/plans/P-1X373873NY326071TNARTBFY/deactivate', 'rel': 'self', 'method': 'POST', 'encType': 'application/json'}]}

#20$ {'id': 'P-17037871PB096542XNARTBNQ', 'product_id': 'PROD-65R61616853458744', 'name': 'Unlimited Monthly Plan', 'status': 'ACTIVE', 'description': 'A simple subscription for $5/month', 'usage_type': 'LICENSED', 'billing_cycles': [{'pricing_scheme': {'version': 1, 'fixed_price': {'currency_code': 'USD', 'value': '20.0'}, 'create_time': '2025-05-13T11:44:54Z', 'update_time': '2025-05-13T11:44:54Z'}, 'frequency': {'interval_unit': 'MONTH', 'interval_count': 1}, 'tenure_type': 'REGULAR', 'sequence': 1, 'total_cycles': 0}], 'payment_preferences': {'service_type': 'PREPAID', 'auto_bill_outstanding': True, 'setup_fee': {'currency_code': 'USD', 'value': '0.0'}, 'setup_fee_failure_action': 'CONTINUE', 'payment_failure_threshold': 3}, 'quantity_supported': False, 'create_time': '2025-05-13T11:44:54Z', 'update_time': '2025-05-13T11:44:54Z', 'links': [{'href': 'https://api.sandbox.paypal.com/v1/billing/plans/P-17037871PB096542XNARTBNQ', 'rel': 'self', 'method': 'GET', 'encType': 'application/json'}, {'href': 'https://api.sandbox.paypal.com/v1/billing/plans/P-17037871PB096542XNARTBNQ', 'rel': 'edit', 'method': 'PATCH', 'encType': 'application/json'}, {'href': 'https://api.sandbox.paypal.com/v1/billing/plans/P-17037871PB096542XNARTBNQ/deactivate', 'rel': 'self', 'method': 'POST', 'encType': 'application/json'}]}