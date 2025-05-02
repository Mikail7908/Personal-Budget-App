from models import Transaction, Budget, SavingsGoal
from datetime import datetime


class TransactionService:
    @staticmethod
    def create_transaction(data):
        try:
            # Create the transaction
            transaction = Transaction(
                amount=float(data["amount"]),
                description=data["description"],
                date=datetime.strptime(data["date"], "%Y-%m-%d"),
                type=data["type"],
                budget_id=data.get("budget_id"),
                savings_goal_id=data.get("savings_goal_id"),
            )
            transaction.validate_amount()
            transaction.save_to_db()

            # This updates the savings goal if a valid savings_goal_id is provided
            if transaction.savings_goal_id:
                savings_goal = SavingsGoal.query.get(transaction.savings_goal_id)
                if savings_goal:
                    savings_goal.current_amount += transaction.amount
                    savings_goal.save_to_db()

            return transaction
        except Exception as e:
            raise Exception(f"Error creating transaction: {str(e)}")

    @staticmethod
    def get_all_transactions():
        try:
            all_transactions = Transaction.fetch_all()
            transaction_list = [
                {
                    "id": transaction.id,
                    "amount": transaction.amount,
                    "description": transaction.description,
                    "date": transaction.date.strftime("%Y-%m-%d"),
                    "type": transaction.type,
                    "budget_id": transaction.budget_id,
                    "savings_goal_id": transaction.savings_goal_id,
                }
                for transaction in all_transactions
            ]
            return transaction_list
        except Exception as e:
            raise Exception(f"Error fetching transactions: {str(e)}")

    @staticmethod
    def update_transaction(transaction_id, data):
        try:
            transaction = Transaction.query.get_or_404(transaction_id)

            # This stores the old values for the transaction
            old_amount = transaction.amount
            old_savings_goal_id = transaction.savings_goal_id

            transaction.amount = float(data["amount"])
            transaction.description = data["description"]
            transaction.date = datetime.strptime(data["date"], "%Y-%m-%d")
            transaction.type = data["type"]
            transaction.budget_id = data.get("budget_id")
            transaction.savings_goal_id = data.get("savings_goal_id")

            transaction.validate_amount()

            transaction.save_to_db(
                old_amount=old_amount,
                old_savings_goal_id=old_savings_goal_id
            )

            return transaction
        except Exception as e:
            raise Exception(f"Error updating transaction: {str(e)}")

    @staticmethod
    def delete_transaction(transaction_id):
        try:
            transaction = Transaction.query.get_or_404(transaction_id)

            if transaction.budget_id:
                budget = Budget.query.get(transaction.budget_id)
                if budget:
                    budget.spent_amount -= transaction.amount
                    budget.save_to_db()

            if transaction.savings_goal_id:
                savings_goal = SavingsGoal.query.get(transaction.savings_goal_id)
                if savings_goal:
                    savings_goal.current_amount -= transaction.amount
                    savings_goal.save_to_db()

            transaction.delete_from_db()

        except Exception as e:
            raise Exception(f"Error deleting transaction: {str(e)}")
