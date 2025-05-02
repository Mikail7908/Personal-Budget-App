import os
import sys
import unittest
from datetime import datetime

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../")))

from main import app, db
from models import Budget, Category
from services.budget_service import BudgetService
from testing.base_test_case import BaseTestCase


class TestBudgetService(BaseTestCase):
    def setUp(self):
        super().setUp()
        test_category = Category(name="Test Category", type="expense")
        db.session.add(test_category)
        db.session.commit()
        self.test_category_id = test_category.id
        test_budget = Budget(
            category_id=self.test_category_id,
            amount=1000.0,
            month="May 2025",
            spent_amount=200.0,
        )
        db.session.add(test_budget)
        db.session.commit()
        self.test_budget_id = test_budget.id

    def test_create_budget(self):
        test_new_budget_data = {
            "category_id": self.test_category_id,
            "amount": "500.0",
            "month": "June 2025",
            "spent_amount": "0.0",
        }

        result = BudgetService.create_budget(test_new_budget_data)
        self.assertIsNotNone(result)
        self.assertEqual(result.amount, 500.0)
        self.assertEqual(result.month, "June 2025")
        saved_budget = Budget.query.filter_by(month="June 2025").first()
        self.assertIsNotNone(saved_budget)

    def test_get_all_budgets(self):
        budgets = BudgetService.get_all_budgets()

        self.assertEqual(len(budgets), 1)
        self.assertEqual(budgets[0]["month"], "May 2025")
        self.assertEqual(budgets[0]["amount"], 1000.0)
        self.assertEqual(budgets[0]["spent_amount"], 200.0)
        self.assertEqual(budgets[0]["remaining"], 800.0)

    def test_update_budget(self):
        update_data = {"amount": "1500.0", "month": "Updated May 2025"}

        result = BudgetService.update_budget(self.test_budget_id, update_data)
        self.assertIsNotNone(result)
        self.assertEqual(result.amount, 1500.0)
        self.assertEqual(result.month, "Updated May 2025")
        updated_budget = Budget.query.get_or_404(self.test_budget_id)
        self.assertEqual(updated_budget.amount, 1500.0)
        self.assertEqual(updated_budget.month, "Updated May 2025")

    def test_delete_budget(self):
        initial_budget_count = len(Budget.query.all())
        BudgetService.delete_budget(self.test_budget_id)
        self.assertEqual(len(Budget.query.all()), initial_budget_count - 1)
        self.assertIsNone(Budget.query.get(self.test_budget_id))


if __name__ == "__main__":
    unittest.main()
