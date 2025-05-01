# services/transaction_service.py
from backend.models import Transaction, Budget, SavingsGoal
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
                savings_goal_id=data.get("savings_goal_id")  # Associate with savings goal if provided
            )
            transaction.validate_amount()
            transaction.save_to_db()

            # Update the budget if a budget ID is provided
            if transaction.budget_id:
                budget = Budget.query.get(transaction.budget_id)
                if budget:
                    budget.spent_amount += transaction.amount
                    budget.save_to_db()
            # Update the savings goal if a savings_goal_id is provided
            if transaction.savings_goal_id:
                savings_goal = SavingsGoal.query.get(transaction.savings_goal_id)
                if savings_goal:
                    savings_goal.current_amount += transaction.amount  # Add amount to savings goal
                    savings_goal.save_to_db()

            return transaction
        except Exception as e:
            raise Exception(f"Error creating transaction: {str(e)}")

    @staticmethod
    def get_all_transactions():
        try:
            all_transactions = Transaction.fetch_all()
            transaction_list = [{
                "id": transaction.id,
                "amount": transaction.amount,
                "description": transaction.description,
                "date": transaction.date.strftime("%Y-%m-%d"),
                "type": transaction.type,
                "budget_id": transaction.budget_id,
                "savings_goal_id": transaction.savings_goal_id
            } for transaction in all_transactions]
            return transaction_list
        except Exception as e:
            raise Exception(f"Error fetching transactions: {str(e)}")

    @staticmethod
    def update_transaction(transaction_id, data):
        try:
            transaction = Transaction.query.get_or_404(transaction_id)

            # Store the old values for the transaction
            old_amount = transaction.amount
            old_savings_goal_id = transaction.savings_goal_id
            old_budget_id = transaction.budget_id

            # Update the transaction data
            transaction.amount = data["amount"]
            transaction.description = data["description"]
            transaction.date = datetime.strptime(data["date"], "%Y-%m-%d")
            transaction.type = data["type"]
            transaction.budget_id = data.get("budget_id")
            transaction.savings_goal_id = data.get("savings_goal_id")

            transaction.validate_amount()

            transaction.save_to_db()

    
            if transaction.budget_id != old_budget_id:
                if old_budget_id:
                    old_budget = Budget.query.get(old_budget_id)
                    if old_budget:
                        old_budget.spent_amount -= old_amount  
                        old_budget.save_to_db()
                if transaction.budget_id:
                    new_budget = Budget.query.get(transaction.budget_id)
                    if new_budget:
                        new_budget.spent_amount += transaction.amount 
                        new_budget.save_to_db()

            
            if old_savings_goal_id != transaction.savings_goal_id:
                if old_savings_goal_id:
                    old_savings_goal = SavingsGoal.query.get(old_savings_goal_id)
                    if old_savings_goal:
                        old_savings_goal.current_amount -= old_amount
                        old_savings_goal.save_to_db()

                if transaction.savings_goal_id:
                    new_savings_goal = SavingsGoal.query.get(transaction.savings_goal_id)
                    if new_savings_goal:
                        new_savings_goal.current_amount += transaction.amount
                        new_savings_goal.save_to_db()

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
