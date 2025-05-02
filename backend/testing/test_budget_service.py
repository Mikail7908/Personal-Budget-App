import os
import sys
import unittest
from datetime import datetime

# Adjusting path so imports work correctly
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../")))

from test_config import create_test_app
from extensions import db
from models import Budget, Category
from services.budget_service import BudgetService

class TestBudgetService(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Sets up the app and database before any tests are run."""
        cls.app = create_test_app()  # Use the helper function to create the test app
        cls.app_context = cls.app.app_context()  # Get the app context
        cls.app_context.push()  # Push the app context

        with cls.app.app_context():
            db.create_all()  # Create all the tables for testing

            # Create a test category and budget to be used in tests
            test_category = Category(name="Test Category", type="expense")
            db.session.add(test_category)
            db.session.commit()
            cls.test_category_id = test_category.id

            test_budget = Budget(
                category_id=cls.test_category_id,
                amount=1000.0,
                month="May 2025",
                spent_amount=200.0
            )
            db.session.add(test_budget)
            db.session.commit()
            cls.test_budget_id = test_budget.id

    @classmethod
    def tearDownClass(cls):
        """Cleans up after all tests have run."""
        with cls.app.app_context():
            db.session.remove()  # Clean up session
            db.drop_all()  # Drop all tables
        cls.app_context.pop()  # Pop the app context

    def test_create_budget(self):
        test_new_budget_data = {
            "category_id": self.test_category_id,
            "amount": "500.0",
            "month": "June 2025",
            "spent_amount": "0.0"
        }

        with self.app.app_context():
            result = BudgetService.create_budget(test_new_budget_data)
            self.assertIsNotNone(result)
            self.assertEqual(result.amount, 500.0)
            self.assertEqual(result.month, "June 2025")
            saved_budget = Budget.query.filter_by(month="June 2025").first()
            self.assertIsNotNone(saved_budget)

    def test_get_all_budgets(self):
        with self.app.app_context():
            budgets = BudgetService.get_all_budgets()
            self.assertEqual(len(budgets), 1)
            self.assertEqual(budgets[0]["month"], "May 2025")
            self.assertEqual(budgets[0]["amount"], 1000.0)
            self.assertEqual(budgets[0]["spent_amount"], 200.0)
            self.assertEqual(budgets[0]["remaining"], 800.0)

    def test_update_budget(self):
        update_data = {
            "amount": "1500.0",
            "month": "Updated May 2025"
        }

        with self.app.app_context():
            result = BudgetService.update_budget(self.test_budget_id, update_data)
            self.assertIsNotNone(result)
            self.assertEqual(result.amount, 1500.0)
            self.assertEqual(result.month, "Updated May 2025")

    def test_delete_budget(self):
        with self.app.app_context():
            initial_budget_count = len(Budget.query.all())
            BudgetService.delete_budget(self.test_budget_id)
            self.assertEqual(len(Budget.query.all()), initial_budget_count - 1)
            self.assertIsNone(Budget.query.get(self.test_budget_id))


if __name__ == "__main__":
    unittest.main()
