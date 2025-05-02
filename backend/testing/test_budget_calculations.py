import sys
import os
import unittest
from datetime import datetime

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../")))

from main import app, db
from models import Budget, Category, Transaction
from testing.base_test_case import BaseTestCase


class TestBudgetCalculations(BaseTestCase):
    def setUp(self):
        super().setUp()
        test_category = Category(name="Food", type="expense")
        db.session.add(test_category)
        db.session.commit()
        self.category_id = test_category.id

        test_budget = Budget(
            category_id=self.category_id,
            amount=1000.0,
            month="May 2025",
            spent_amount=0.0,
        )
        db.session.add(test_budget)
        db.session.commit()
        self.budget_id = test_budget.id

    def test_calculate_remaining(self):
        budget = Budget.query.get(self.budget_id)
        self.assertEqual(budget.calculate_remaining(), 1000.0)

        # This adds some expenses to the budget
        budget.spent_amount = 250.0
        db.session.commit()
        self.assertEqual(budget.calculate_remaining(), 750.0)

        # This adds even more expenses to test going over the budget
        budget.spent_amount = 1200.0
        db.session.commit()
        self.assertEqual(budget.calculate_remaining(), -200.0)

    def test_budget_with_multiple_transactions(self):
        for i in range(1, 6):
            transaction = Transaction(
                amount=100.0 * i,
                description=f"Transaction {i}",
                date=datetime.now(),
                type="expense",
                budget_id=self.budget_id,
            )
            transaction.save_to_db()

        budget = Budget.query.get(self.budget_id)
        self.assertEqual(budget.spent_amount, 1500.0)
        self.assertEqual(budget.calculate_remaining(), -500.0)


if __name__ == "__main__":
    unittest.main()