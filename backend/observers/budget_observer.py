class BudgetObserver:
    @staticmethod
    def update_budget_on_transaction_update(transaction, old_amount=None, new_amount=None):
        from backend.models import Budget
        
        if transaction.budget_id:
            budget = Budget.query.get(transaction.budget_id)
            
            if budget:
                if old_amount is None and new_amount is not None:
                    budget.spent_amount += new_amount
                elif old_amount is not None and new_amount is not None:
                    budget.spent_amount = budget.spent_amount - old_amount + new_amount
                elif old_amount is not None and new_amount is None:
                    budget.spent_amount -= old_amount
                    
                budget.spent_amount = max(budget.spent_amount, 0)
                budget.save_to_db()