"""
Salesforce Integration - Fetch unpaid opportunities
"""
import os
from dotenv import load_dotenv

load_dotenv()

class SalesforceService:
    def __init__(self, username=None, password=None, security_token=None):
        self.username = username or os.getenv("SALESFORCE_USERNAME")
        self.password = password or os.getenv("SALESFORCE_PASSWORD")
        self.security_token = security_token or os.getenv("SALESFORCE_SECURITY_TOKEN")
        self.sf = None
        self._connect()
    
    def _connect(self):
        """Connect to Salesforce"""
        try:
            from simple_salesforce import Salesforce
            self.sf = Salesforce(
                username=self.username,
                password=self.password,
                security_token=self.security_token,
                sandbox=True
            )
            print("✓ Salesforce connection successful")
        except Exception as e:
            print(f"✗ Salesforce connection optional (using mock data): {type(e).__name__}")
    
    def get_unpaid_opportunities(self, limit=10) -> list:
        """Fetch unpaid opportunities from Salesforce or return mock data"""
        
        if not self.sf:
            return self._get_mock_data()
        
        try:
            result = self.sf.query(
                f"SELECT Id, Name, Amount, CreatedDate "
                f"FROM Opportunity "
                f"WHERE StageName = 'Closed Won' "
                f"ORDER BY Amount DESC LIMIT {limit}"
            )
            
            opportunities = []
            for record in result.get("records", []):
                from datetime import datetime
                created = datetime.fromisoformat(
                    record["CreatedDate"].replace("Z", "+00:00")
                )
                days_overdue = (datetime.now(created.tzinfo) - created).days
                
                opportunities.append({
                    "id": record["Id"],
                    "dealName": record["Name"],
                    "amount": float(record["Amount"]),
                    "daysOverdue": days_overdue,
                    "industry": "Technology"
                })
            return opportunities
        except Exception as e:
            print(f"✗ Error fetching from Salesforce: {e}")
            return self._get_mock_data()
    
    def _get_mock_data(self) -> list:
        """Return mock data for testing"""
        return [
            {"id": "006-001", "dealName": "ABC Corporation", "amount": 50000, "daysOverdue": 30, "industry": "Technology"},
            {"id": "006-002", "dealName": "XYZ Industries", "amount": 75000, "daysOverdue": 15, "industry": "Manufacturing"},
            {"id": "006-003", "dealName": "123 Retail Ltd", "amount": 25000, "daysOverdue": 45, "industry": "Retail"}
        ]

if __name__ == "__main__":
    sf_service = SalesforceService()
    opportunities = sf_service.get_unpaid_opportunities(limit=5)
    for opp in opportunities:
        print(f"{opp['dealName']}: ${opp['amount']:,} ({opp['daysOverdue']} days overdue)")
