import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../")))

import unittest
from datetime import datetime
from backend.main import app, db
from backend.models import  Transaction, Budget
from backend.services.transaction_service import TransactionService

class TestTransactionService(unittest.TestCase):
    def setUp(self):
        app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
        app.config["TESTING"] = True
        self.app_context = app.app_context()
        self.app_context.push()
        with app.app_context():
            db.create_all()
            self.budget = Budget(
                category_id=1,
                amount=1000.0,
                month="April 2025",
                spent_amount=0.0
            )
        db.session.add(self.budget)
        db.session.commit()
        self.client = app.test_client()
    
    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()
    
    def test_update_transaction_updates_budget(self):
        with app.app_context():
            test_data = {
                "amount": "200",
                "description": "Test transaction",
                "date": "2025-04-10",
                "type": "expense",
                "budget_id": self.budget.id
            }
            test_transaction = TransactionService.create_transaction(test_data)
            original_spent = Budget.query.get(self.budget.id).spent_amount
            update_test_data = {
                "amount": "300",
                "description": "Updated test transaction",
                "date": "2025-04-10",
                "type": "expense",
                "budget_id": self.budget.id
            }
            updated_transaction = TransactionService.update_transaction(test_transaction.id, update_test_data)
            updated_budget = Budget.query.get(self.budget.id)
            self.assertEqual(updated_transaction.amount, 300.0)
            self.assertEqual(updated_budget.spent_amount, original_spent - 200.0 + 300.0)
            
    def test_delete_transaction_updates_budget(self):
        with app.app_context():
            test_data = {
                "amount": "100",
                "description": "Testing delete transaction",
                "date": "2025-04-10",
                "type": "expense",
                "budget_id": self.budget.id
            }
            test_transaction = TransactionService.create_transaction(test_data)
            budget_after_creation =  Budget.query.get(self.budget.id)
            spent_amount_after_creation = budget_after_creation.spent_amount
            TransactionService.delete_transaction(test_transaction.id)
            updated_budget = Budget.query.get(self.budget.id)
            self.assertEqual(updated_budget.spent_amount, spent_amount_after_creation - 100.0)


if __name__ == "__main__":
    unittest.main()
            