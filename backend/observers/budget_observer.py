class BudgetObserver:
    @staticmethod
    def update_budget_on_transaction_update(transaction, old_amount=None, new_amount=None):
        from models import Budget
        
        if transaction.budget_id:
            budget = Budget.query.get(transaction.budget_id)
            
            if budget:
                # This subracts the old value if there's an old amount (e.g when updating)
                if old_amount is not None:
                    budget.spent_amount = budget.spent_amount - old_amount + transaction.amount
                else:
                    budget.spent_amount += transaction.amount
                budget.spent_amount = max(budget.spent_amount, 0)
                budget.save_to_db()

