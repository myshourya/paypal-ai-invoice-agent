"""
Smart Payment Agent - Mock version (API will be swapped in later)
"""
import json
import os
from dotenv import load_dotenv

load_dotenv()

class SmartPaymentAgent:
    def __init__(self):
        print("✓ Payment Agent initialized (mock mode)")
        
    def analyze_invoice(self, invoice: dict) -> dict:
        """Returns AI-like recommendations (mock)"""
        
        days_overdue = invoice.get('daysOverdue', 0)
        amount = invoice.get('amount', 0)
        
        # Mock logic
        if days_overdue > 30 and amount > 40000:
            priority = "HIGH"
            discount = 10
            plan = "30% now, 70% in 60 days"
        elif days_overdue > 15:
            priority = "MEDIUM"
            discount = 5
            plan = "50% now, 50% in 30 days"
        else:
            priority = "LOW"
            discount = 0
            plan = "Full payment due"
        
        return {
            "invoice_id": invoice.get('id'),
            "priority": priority,
            "payment_plan": plan,
            "discount_percentage": discount,
            "follow_up_action": "email + SMS reminder",
            "reasoning": f"Days overdue: {days_overdue}, Amount: ${amount:,}"
        }


if __name__ == "__main__":
    agent = SmartPaymentAgent()
    invoice = {"id": "006-ABC-001", "dealName": "ABC Corp", "amount": 50000, "daysOverdue": 30}
    print("\nAnalyzing invoice...")
    result = agent.analyze_invoice(invoice)
    print(json.dumps(result, indent=2))
