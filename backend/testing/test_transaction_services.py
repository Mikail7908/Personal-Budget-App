import sys
import os
import unittest
from datetime import datetime

# Adjust path so imports work correctly
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../")))

from test_config import create_test_app
from models import Transaction, Budget
from services.transaction_service import TransactionService
from extensions import db  # Import db object from extensions

class TestTransactionService(unittest.TestCase):
    def setUp(self):
        # Use the helper function from test_config to set up the test app
        self.app = create_test_app()
        self.app_context = self.app.app_context()
        self.app_context.push()
        with self.app.app_context():
            db.create_all()

            # Create a test budget to associate with transactions
            test_budget = Budget(
                category_id=1,
                amount=1000.0,
                month="April 2025",
                spent_amount=0.0
            )
            db.session.add(test_budget)
            db.session.commit()
            self.test_budget_id = test_budget.id
            self.client = self.app.test_client()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()
        self.app_context.pop()

    def test_create_transaction(self):
        test_data = {
            "amount": "150.0",
            "description": "Test transaction creation",
            "date": "2025-04-10",
            "type": "expense",
            "budget_id": self.test_budget_id
        }
        initial_budget = Budget.query.get(self.test_budget_id)
        self.assertEqual(initial_budget.spent_amount, 0.0)

        result = TransactionService.create_transaction(test_data)
        self.assertIsNotNone(result)
        self.assertEqual(result.amount, 150.0)

        updated_budget = Budget.query.get(self.test_budget_id)
        self.assertEqual(updated_budget.spent_amount, 150.0)

    def test_update_transaction_updates_budget(self):
        test_data = {
            "amount": "200.0",
            "description": "Test transaction",
            "date": "2025-04-10",
            "type": "expense",
            "budget_id": self.test_budget_id
        }

        initial_budget = Budget.query.get(self.test_budget_id)
        self.assertEqual(initial_budget.spent_amount, 0.0)

        test_transaction = TransactionService.create_transaction(test_data)
        budget_after_creation = Budget.query.get(self.test_budget_id)
        self.assertEqual(budget_after_creation.spent_amount, 200.0)

        update_test_data = {
            "amount": "300.0",
            "description": "Updated test transaction",
            "date": "2025-04-10",
            "type": "expense",
            "budget_id": self.test_budget_id
        }
        updated_transaction = TransactionService.update_transaction(test_transaction.id, update_test_data)
        updated_budget = Budget.query.get(self.test_budget_id)
        self.assertEqual(updated_budget.spent_amount, 300.0)

    def test_delete_transaction_updates_budget(self):
        test_data = {
            "amount": "100.0",
            "description": "Testing delete transaction",
            "date": "2025-04-10",
            "type": "expense",
            "budget_id": self.test_budget_id
        }

        initial_budget = Budget.query.get(self.test_budget_id)
        self.assertEqual(initial_budget.spent_amount, 0.0)

        test_transaction = TransactionService.create_transaction(test_data)
        budget_after_creation = Budget.query.get(self.test_budget_id)
        self.assertEqual(budget_after_creation.spent_amount, 100.0)

        TransactionService.delete_transaction(test_transaction.id)
        updated_budget = Budget.query.get(self.test_budget_id)
        self.assertEqual(updated_budget.spent_amount, 0.0)
        self.assertIsNone(Transaction.query.get(test_transaction.id))

if __name__ == "__main__":
    unittest.main()
