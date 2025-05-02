import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../")))

import unittest
from datetime import datetime, timedelta
from main import app, db
from models import Transaction, Budget, SavingsGoal, Category
from testing.base_test_case import BaseTestCase


class TestModels(BaseTestCase):
    def test_transaction_creation(self):
        test_transaction = Transaction(
            amount=100.0,
            description="Test",
            type="expense",
            date=datetime.now(),
        )
        test_transaction.save_to_db()
        transaction = Transaction.query.first()
        self.assertIsNotNone(transaction)
        self.assertEqual(transaction.amount, 100.0)
        self.assertEqual(transaction.description, "Test")
        self.assertEqual(transaction.type, "expense")

    def test_budget_creation(self):
        test_category = Category(
            name="Test Category", type="expense", date=datetime.now()
        )
        test_category.save_to_db()
        test_budget = Budget(
            category_id=test_category.id,
            amount=500.0,
            month="April",
            spent_amount=0.0,
            date=datetime.now(),
        )
        test_budget.save_to_db()
        budget = Budget.query.first()
        self.assertIsNotNone(budget)
        self.assertEqual(budget.amount, 500.0)
        self.assertEqual(budget.month, "April")
        self.assertEqual(budget.spent_amount, 0.0)
        self.assertEqual(budget.category_id, test_category.id)

    def test_category_creation(self):
        test_category = Category(name="Food", type="expense", date=datetime.now())
        test_category.save_to_db()

        category = Category.query.first()
        self.assertIsNotNone(category)
        self.assertEqual(category.name, "Food")
        self.assertEqual(category.type, "expense")

    def test_savings_goal_creation(self):
        deadline = datetime.now() + timedelta(days=30)
        test_goal = SavingsGoal(
            target_amount=1000.0,
            current_amount=250.0,
            deadline=deadline,
            description="Vacation Fund",
            saving_frequency="monthly",
            date=datetime.now(),
        )
        test_goal.save_to_db()

        goal = SavingsGoal.query.first()
        self.assertIsNotNone(goal)
        self.assertEqual(goal.target_amount, 1000.0)
        self.assertEqual(goal.current_amount, 250.0)
        self.assertEqual(goal.description, "Vacation Fund")
        self.assertEqual(goal.saving_frequency, "monthly")


if __name__ == "__main__":
    unittest.main()