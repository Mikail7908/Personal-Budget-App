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
    def get_all_savings_goals():
        try:
            all_goals = SavingsGoal.fetch_all()
            goals_list = [{
                "id": goal.id,
                "target_amount": goal.target_amount,
                "current_amount": goal.current_amount,
                "deadline": goal.deadline.strftime("%Y-%m-%d"),
                "description": goal.description,
                "saving_frequency": goal.saving_frequency,
                "progress": goal.calculate_progress()
            } for goal in all_goals]
            return goals_list
        except Exception as e:
            raise Exception(f"Error fetching savings goals: {str(e)}")

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
            SavingsGoal.delete(goal_id)
        except Exception as e:
            raise Exception(f"Error deleting savings goal: {str(e)}")
