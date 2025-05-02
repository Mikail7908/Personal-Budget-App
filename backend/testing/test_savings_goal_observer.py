import sys
import os
from datetime import datetime, timedelta
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../")))

import unittest
from main import db
from models import Transaction, SavingsGoal
from observers.savings_goal_observer import SavingsGoalObserver
from testing.base_test_case import BaseTestCase


class TestSavingsGoalObserver(BaseTestCase):
    def setUp(self):
        super().setUp()
        
        test_goal = SavingsGoal(
            target_amount=1000.0,
            current_amount=0.0,
            deadline=datetime.now() + timedelta(days=30),
            description="Test Savings Goal",
            saving_frequency="monthly"
        )
        db.session.add(test_goal)
        db.session.commit()
        self.test_goal_id = test_goal.id
        
        second_goal = SavingsGoal(
            target_amount=2000.0,
            current_amount=0.0,
            deadline=datetime.now() + timedelta(days=60),
            description="Second Savings Goal",
            saving_frequency="weekly"
        )
        db.session.add(second_goal)
        db.session.commit()
        self.second_goal_id = second_goal.id
    
    def test_update_goal_on_transaction_creation(self):
        transaction = Transaction(
            amount=200.0,
            description="Test savings transaction",
            date=datetime.now(),
            type="savings",
            savings_goal_id=self.test_goal_id
        )
        transaction.save_to_db()
        
        updated_goal = db.session.get(SavingsGoal, self.test_goal_id)
        self.assertEqual(updated_goal.current_amount, 200.0)
        
    def test_update_goal_on_transaction_update(self):
        transaction = Transaction(
            amount=300.0,
            description="Test update transaction",
            date=datetime.now(),
            type="savings",
            savings_goal_id=self.test_goal_id
        )
        transaction.save_to_db()
        
        goal_after_creation = db.session.get(SavingsGoal, self.test_goal_id)
        self.assertEqual(goal_after_creation.current_amount, 300.0)
        
        old_amount = transaction.amount
        transaction.amount = 500.0
        transaction.save_to_db(
            old_amount=old_amount,
            old_savings_goal_id=transaction.savings_goal_id
        )
        
        updated_goal = db.session.get(SavingsGoal, self.test_goal_id)
        self.assertEqual(updated_goal.current_amount, 500.0)
        
    def test_update_goal_on_transaction_delete(self):
        transaction = Transaction(
            amount=150.0,
            description="Test delete transaction",
            date=datetime.now(),
            type="savings",
            savings_goal_id=self.test_goal_id
        )
        transaction.save_to_db()
        
        goal_after_creation = db.session.get(SavingsGoal, self.test_goal_id)
        self.assertEqual(goal_after_creation.current_amount, 150.0)
        
        old_amount = transaction.amount
        old_goal_id = transaction.savings_goal_id
        transaction.amount = 0.0
        
        SavingsGoalObserver.update_goal_on_transaction_update(
            transaction, 
            old_amount=old_amount,
            old_savings_goal_id=old_goal_id
        )
        
        updated_goal = db.session.get(SavingsGoal, self.test_goal_id)
        self.assertEqual(updated_goal.current_amount, 0.0)
    
    def test_transfer_between_savings_goals(self):
        transaction = Transaction(
            amount=250.0,
            description="Initial allocation",
            date=datetime.now(),
            type="savings",
            savings_goal_id=self.test_goal_id
        )
        transaction.save_to_db()
        
        first_goal = db.session.get(SavingsGoal, self.test_goal_id)
        self.assertEqual(first_goal.current_amount, 250.0)
        
        old_amount = transaction.amount
        old_goal_id = transaction.savings_goal_id
        transaction.savings_goal_id = self.second_goal_id
        
        SavingsGoalObserver.update_goal_on_transaction_update(
            transaction, 
            old_amount=old_amount,
            old_savings_goal_id=old_goal_id
        )
        
        updated_first_goal = db.session.get(SavingsGoal, self.test_goal_id)
        updated_second_goal = db.session.get(SavingsGoal, self.second_goal_id)
        
        self.assertEqual(updated_first_goal.current_amount, 0.0)
        self.assertEqual(updated_second_goal.current_amount, 250.0)
    
    def test_handle_missing_savings_goal(self):
        transaction = Transaction(
            amount=100.0,
            description="Invalid goal transaction",
            date=datetime.now(),
            type="savings",
            savings_goal_id=9999
        )
        
        SavingsGoalObserver.update_goal_on_transaction_update(transaction)


if __name__ == "__main__":
    unittest.main()