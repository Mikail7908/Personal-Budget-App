class BudgetObserver:
    @staticmethod
    def update_budget_on_transaction_update(transaction, old_amount=None):
        from models import Budget
        if transaction.budget_id:
            budget = Budget.query.get(transaction.budget_id)
            if budget:
                # If there's an old amount (e.g., when updating a transaction), subtract the old value
                if old_amount is not None:
                    budget.spent_amount -= old_amount

                # Add the new transaction amount
                budget.spent_amount += transaction.amount
                budget.spent_amount = max(budget.spent_amount, 0)  # Ensure non-negative spent amount
                budget.save_to_db()
