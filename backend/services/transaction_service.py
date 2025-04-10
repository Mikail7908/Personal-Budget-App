from backend.models import Transaction, Budget
from datetime import datetime
from backend.observers.budget_observer import BudgetObserver


class TransactionService:
    @staticmethod
    def create_transaction(data):
        transaction = Transaction(
            amount=float(data["amount"]),
            description=data["description"],
            date=datetime.strptime(data["date"], "%Y-%m-%d"),
            type=data["type"],
            budget_id=data.get("budget_id")
        )
        transaction.validate_amount()
        transaction.save_to_db()
        return transaction
    
    @staticmethod
    def get_all_transactions():
        all_transactions = Transaction.fetch_all()
        transaction_list = [{
            "id": transaction.id,
            "amount": transaction.amount,
            "description": transaction.description,
            "date": transaction.date.strftime("%Y-%m-%d"),
            "type": transaction.type,
            "budget_id": transaction.budget_id
        } for transaction in all_transactions]
        return transaction_list
    
    @staticmethod
    def update_transaction(transaction_id, data):
        transaction = Transaction.query.get_or_404(transaction_id)

        # Store original values
        old_budget_id = transaction.budget_id
        old_amount = float(transaction.amount)

        # Update with new data
        transaction.amount = float(data["amount"])
        transaction.description = data["description"]
        transaction.date = datetime.strptime(data["date"], "%Y-%m-%d")
        transaction.type = data["type"]
        transaction.budget_id = data.get("budget_id")
        
        transaction.validate_amount()
        transaction.save_to_db(old_amount=old_amount)
        
        # BudgetObserver.update_budget_on_transaction_update(transaction, old_amount, new_amount=transaction.amount)
        return transaction
    
    @staticmethod
    def delete_transaction(transaction_id):
        transaction = Transaction.query.get_or_404(transaction_id)
        transaction.delete_from_db()
        