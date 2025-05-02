from models import Budget, Category
from datetime import datetime


class BudgetService:
    @staticmethod
    def create_budget(data):
        try:
            spent_amount = float(data.get("spent_amount", "0.0"))
            budget = Budget(
                category_id=data["category_id"],
                amount=float(data["amount"]),
                month=data["month"],
                spent_amount=spent_amount,
            )
            budget.save_to_db()
            return budget
        except Exception as e:
            raise Exception(f"Error creating budget: {str(e)}")

    @staticmethod
    def get_all_budgets():
        try:
            all_budgets = Budget.fetch_all()
            budget_list = [
                {
                    "id": budget.id,
                    "category_id": budget.category_id,
                    "category_name": budget.category.name if budget.category else None,
                    "amount": budget.amount,
                    "month": budget.month,
                    "spent_amount": budget.spent_amount,
                    "remaining": budget.calculate_remaining(),
                }
                for budget in all_budgets
            ]
            return budget_list
        except Exception as e:
            raise Exception(f"Error fetching budgets: {str(e)}")

    @staticmethod
    def update_budget(budget_id, data):
        try:
            budget = Budget.query.get_or_404(budget_id)
            budget.amount = float(data["amount"])
            budget.month = data["month"]
            if "category_id" in data:
                budget.category_id = data["category_id"]
            budget.save_to_db()
            return budget
        except Exception as e:
            raise Exception(f"Error updating budget: {str(e)}")

    @staticmethod
    def delete_budget(budget_id):
        try:
            Budget.delete(budget_id)
        except Exception as e:
            raise Exception(f"Error deleting budget: {str(e)}")
