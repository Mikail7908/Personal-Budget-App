class SavingsGoalObserver:
    @staticmethod
    def update_goal_on_transaction_update(
        transaction, old_amount=None, old_savings_goal_id=None
    ):
        from models import SavingsGoal
        from extensions import db
        
        # Case 1: New transaction
        if old_amount is None:
            if transaction.savings_goal_id:
                goal = db.session.get(SavingsGoal, transaction.savings_goal_id)
                if goal:
                    goal.current_amount += transaction.amount
                    db.session.commit()
            return
            
        # Case 2: Transaction moved between goals
        if old_savings_goal_id and old_savings_goal_id != transaction.savings_goal_id:
            # Remove from old goal
            old_goal = db.session.get(SavingsGoal, old_savings_goal_id)
            if old_goal:
                old_goal.current_amount -= old_amount
                db.session.commit()
                
            # Add to new goal
            if transaction.savings_goal_id:
                new_goal = db.session.get(SavingsGoal, transaction.savings_goal_id)
                if new_goal:
                    new_goal.current_amount += transaction.amount
                    db.session.commit()
            return
            
        # Case 3: Amount changed for same goal
        if transaction.savings_goal_id:
            goal = db.session.get(SavingsGoal, transaction.savings_goal_id) 
            if goal:
                goal.current_amount = goal.current_amount - old_amount + transaction.amount
                db.session.commit()