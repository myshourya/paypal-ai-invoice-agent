"""
PayPal Sandbox Integration
"""
import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

class PayPalService:
    def __init__(self, client_id=None, secret=None):
        self.client_id = client_id or os.getenv("PAYPAL_CLIENT_ID")
        self.secret = secret or os.getenv("PAYPAL_SECRET")
        self.sandbox_url = "https://api.sandbox.paypal.com"
        self.access_token = None
        self._get_access_token()
    
    def _get_access_token(self):
        """Get OAuth token from PayPal"""
        url = f"{self.sandbox_url}/v1/oauth2/token"
        
        try:
            response = requests.post(
                url,
                auth=(self.client_id, self.secret),
                data={"grant_type": "client_credentials"},
                timeout=10
            )
            
            if response.status_code == 200:
                self.access_token = response.json()["access_token"]
                print("✓ PayPal authentication successful")
            else:
                print(f"✗ PayPal auth failed: {response.text}")
        except Exception as e:
            print(f"✗ PayPal connection error: {e}")
    
    def create_payment_link(self, invoice_id: str, amount: float, 
                           deal_name: str, payment_plan: str = "") -> dict:
        """Create a PayPal checkout link for payment"""
        
        if not self.access_token:
            return {"success": False, "error": "Not authenticated with PayPal"}
        
        url = f"{self.sandbox_url}/v2/checkout/orders"
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "intent": "CAPTURE",
            "purchase_units": [{
                "reference_id": invoice_id,
                "description": f"{deal_name} - Invoice Payment",
                "amount": {
                    "currency_code": "USD",
                    "value": str(amount)
                },
                "custom_id": invoice_id
            }],
            "application_context": {
                "return_url": "https://example.com/return",
                "cancel_url": "https://example.com/cancel"
            }
        }
        
        try:
            response = requests.post(url, headers=headers, json=payload, timeout=10)
            
            if response.status_code == 201:
                order_data = response.json()
                approval_link = None
                for link in order_data.get("links", []):
                    if link.get("rel") == "approve":
                        approval_link = link.get("href")
                        break
                
                return {
                    "success": True,
                    "order_id": order_data.get("id"),
                    "payment_link": approval_link,
                    "status": order_data.get("status")
                }
            else:
                return {"success": False, "error": f"PayPal error: {response.text}"}
        except Exception as e:
            return {"success": False, "error": str(e)}

if __name__ == "__main__":
    service = PayPalService()
    result = service.create_payment_link(
        invoice_id="006-ABC-001",
        amount=50000,
        deal_name="ABC Corporation"
    )
    print(json.dumps(result, indent=2))
