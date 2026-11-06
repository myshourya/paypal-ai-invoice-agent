"""
Full end-to-end demo
"""
import json
import sys
sys.path.insert(0, 'src')

from agent import SmartPaymentAgent
from paypal_service import PayPalService
from salesforce_service import SalesforceService

def main():
    print("=" * 60)
    print("PayPal + AI Invoice Agent - Demo")
    print("=" * 60)
    
    print("\n[1] Fetching unpaid invoices from Salesforce...")
    sf_service = SalesforceService()
    invoices = sf_service.get_unpaid_opportunities(limit=3)
    print(f"✓ Found {len(invoices)} unpaid invoices\n")
    
    print("[2] Analyzing invoices with AI agent...")
    agent = SmartPaymentAgent()
    
    print("\n[3] Creating PayPal payment links...")
    paypal = PayPalService()
    
    results = []
    for invoice in invoices:
        print(f"\n  Processing: {invoice['dealName']}")
        
        recommendation = agent.analyze_invoice(invoice)
        print(f"  ✓ AI Priority: {recommendation.get('priority')}")
        print(f"  ✓ AI Plan: {recommendation.get('payment_plan')}")
        print(f"  ✓ AI Discount: {recommendation.get('discount_percentage')}%")
        
        paypal_result = paypal.create_payment_link(
            invoice_id=invoice["id"],
            amount=invoice["amount"],
            deal_name=invoice["dealName"],
            payment_plan=recommendation.get("payment_plan")
        )
        
        if paypal_result.get("success"):
            print(f"  ✓ PayPal Link: {paypal_result.get('payment_link')}")
        else:
            print(f"  ✗ PayPal Error: {paypal_result.get('error')}")
        
        results.append({
            "invoice": invoice,
            "recommendation": recommendation,
            "paypal": paypal_result
        })
    
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(json.dumps(results, indent=2, default=str))
    print("\n✓ Demo completed!")

if __name__ == "__main__":
    main()
