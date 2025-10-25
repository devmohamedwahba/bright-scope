import requests
from django.conf import settings

class PayTabsService:
    def __init__(self):
        self.api_url = f"{settings.PAYTABS_BASE_URL}/payment/request"
        self.headers = {
            "Authorization": f"{settings.PAYTABS_SERVER_KEY}",
            "Content-Type": "application/json"
        }

    def create_payment_session(self, payment):
        """Create a PayTabs payment session."""
        callback_url = settings.PAYTABS_CALLBACK_PATH
        return_url = settings.PAYTABS_RETURN_PATH

        payload = {
            "profile_id": settings.PAYTABS_PROFILE_ID,
            "tran_type": "sale",
            "tran_class": "ecom",
            "cart_id": str(payment.order_id),
            "cart_currency": payment.currency,
            "cart_amount": str(payment.amount),
            "cart_description": f"Payment for order {payment.order_id}",
            "callback": callback_url,
            "return": return_url,
            "customer_details": {
                "name": payment.customer_name,
                "email": payment.customer_email,
                "street1": "Not Provided",
                "city": "Dubai",
                "country": "AE",
                "ip": "0.0.0.0"
            },
        }

        response = requests.post(self.api_url, json=payload, headers=self.headers, timeout=15)
        response.raise_for_status()  # raises on 4xx/5xx
        return response.json()

    def verify_payment(self, tran_ref):
        """Optional: verify a transaction using PayTabs API."""
        url = f"{settings.PAYTABS_BASE_URL}/payment/query"
        payload = {"tran_ref": tran_ref, "profile_id": settings.PAYTABS_PROFILE_ID}
        response = requests.post(url, json=payload, headers=self.headers)
        response.raise_for_status()
        return response.json()
