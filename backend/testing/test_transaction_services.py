import sys
import os
import unittest
from datetime import datetime

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../")))

from main import app, db
from models import Transaction, Budget
from services.transaction_service import TransactionService
from testing.base_test_case import BaseTestCase


class TestTransactionService(BaseTestCase):
    def setUp(self):
        super().setUp()
        test_budget = Budget(
            category_id=1, amount=1000.0, month="April 2025", spent_amount=0.0
        )
        db.session.add(test_budget)
        db.session.commit()
        self.test_budget_id = test_budget.id
        self.client = app.test_client()

    def test_create_transaction(self):
        test_data = {
            "amount": "150.0",
            "description": "Test transaction creation",
            "date": "2025-04-10",
            "type": "expense",
            "budget_id": self.test_budget_id,
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
            "budget_id": self.test_budget_id,
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
            "budget_id": self.test_budget_id,
        }
        updated_transaction = TransactionService.update_transaction(
            test_transaction.id, update_test_data
        )
        updated_budget = Budget.query.get(self.test_budget_id)
        self.assertEqual(updated_budget.spent_amount, 300.0)

    def test_delete_transaction_updates_budget(self):
        test_data = {
            "amount": "100.0",
            "description": "Testing delete transaction",
            "date": "2025-04-10",
            "type": "expense",
            "budget_id": self.test_budget_id,
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
