# services/savings_goal_service.py
from models import SavingsGoal
from datetime import datetime

class SavingsGoalService:
    @staticmethod
    def create_savings_goal(data):
        try:
            new_goal = SavingsGoal(
                target_amount=float(data["target_amount"]),
                current_amount=float(data.get("current_amount", 0)),
                deadline=datetime.strptime(data["deadline"], "%Y-%m-%d"),
                description=data["description"],
                saving_frequency=data["saving_frequency"]
            )
            new_goal.save_to_db()
            return new_goal
        except Exception as e:
            raise Exception(f"Error creating savings goal: {str(e)}")

    @staticmethod
    def update_savings_goal(goal_id, data):
        try:
            goal = SavingsGoal.query.get_or_404(goal_id)
            goal.target_amount = float(data["target_amount"])
            goal.current_amount = float(data.get("current_amount", goal.current_amount))
            goal.deadline = datetime.strptime(data["deadline"], "%Y-%m-%d")
            goal.description = data["description"]
            goal.saving_frequency = data["saving_frequency"]
            goal.save_to_db()
            return goal
        except Exception as e:
            raise Exception(f"Error updating savings goal: {str(e)}")

    @staticmethod
    def delete_savings_goal(goal_id):
        try:
            goal = SavingsGoal.query.get_or_404(goal_id)
            goal.delete_from_db()
        except Exception as e:
            raise Exception(f"Error deleting savings goal: {str(e)}")
