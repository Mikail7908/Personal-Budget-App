import os
import sys
import unittest
from datetime import datetime, timedelta

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../")))

from main import app, db
from models import SavingsGoal
from services.savings_goal_service import SavingsGoalService
from testing.base_test_case import BaseTestCase


class TestSavingsGoalService(BaseTestCase):
    def setUp(self):
        super().setUp()

        test_deadline = datetime.now() + timedelta(days=30)
        test_goal = SavingsGoal(
            target_amount=1000.0,
            current_amount=250.0,
            deadline=test_deadline,
            description="Test Savings Goal",
            saving_frequency="monthly",
        )
        db.session.add(test_goal)
        db.session.commit()
        self.test_goal_id = test_goal.id
        self.test_deadline = test_deadline

    def test_create_savings_goal(self):
        test_new_goal_data = {
            "target_amount": "500.0",
            "current_amount": "100.0",
            "deadline": (datetime.now() + timedelta(days=60)).strftime("%Y-%m-%d"),
            "description": "New Test Savings Goal",
            "saving_frequency": "weekly",
        }

        result = SavingsGoalService.create_savings_goal(test_new_goal_data)
        self.assertIsNotNone(result)
        self.assertEqual(result.target_amount, 500.0)
        self.assertEqual(result.current_amount, 100.0)
        self.assertEqual(result.description, "New Test Savings Goal")
        self.assertEqual(result.saving_frequency, "weekly")

        saved_goal = SavingsGoal.query.filter_by(
            description="New Test Savings Goal"
        ).first()
        self.assertIsNotNone(saved_goal)

    def test_get_all_savings_goals(self):
        goals = SavingsGoalService.get_all_savings_goals()

        self.assertEqual(len(goals), 1)
        self.assertEqual(goals[0]["description"], "Test Savings Goal")
        self.assertEqual(goals[0]["target_amount"], 1000.0)
        self.assertEqual(goals[0]["current_amount"], 250.0)
        self.assertEqual(goals[0]["saving_frequency"], "monthly")
        self.assertEqual(goals[0]["progress"], 25.0)

    def test_update_savings_goal(self):
        update_data = {
            "target_amount": "2000.0",
            "current_amount": "500.0",
            "deadline": (datetime.now() + timedelta(days=90)).strftime("%Y-%m-%d"),
            "description": "Updated Savings Goal",
            "saving_frequency": "weekly",
        }

        result = SavingsGoalService.update_savings_goal(self.test_goal_id, update_data)
        self.assertIsNotNone(result)
        self.assertEqual(result.target_amount, 2000.0)
        self.assertEqual(result.current_amount, 500.0)
        self.assertEqual(result.description, "Updated Savings Goal")
        self.assertEqual(result.saving_frequency, "weekly")

        updated_goal = SavingsGoal.query.get_or_404(self.test_goal_id)
        self.assertEqual(updated_goal.target_amount, 2000.0)
        self.assertEqual(updated_goal.current_amount, 500.0)
        self.assertEqual(updated_goal.description, "Updated Savings Goal")
        self.assertEqual(updated_goal.calculate_progress(), 25.0)

    def test_delete_savings_goal(self):
        initial_goal_count = len(SavingsGoal.query.all())
        SavingsGoalService.delete_savings_goal(self.test_goal_id)
        self.assertEqual(len(SavingsGoal.query.all()), initial_goal_count - 1)
        self.assertIsNone(SavingsGoal.query.get(self.test_goal_id))

    def test_progress_calculation(self):
        goals = SavingsGoalService.get_all_savings_goals()
        self.assertEqual(goals[0]["progress"], 25.0)

        update_data = {
            "target_amount": "1000.0",
            "current_amount": "750.0",
            "deadline": self.test_deadline.strftime("%Y-%m-%d"),
            "description": "Test Savings Goal",
            "saving_frequency": "monthly",
        }

        SavingsGoalService.update_savings_goal(self.test_goal_id, update_data)
        updated_goals = SavingsGoalService.get_all_savings_goals()
        self.assertEqual(updated_goals[0]["progress"], 75.0)


if __name__ == "__main__":
    unittest.main()