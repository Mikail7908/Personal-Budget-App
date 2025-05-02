import sys
import os
import unittest
from datetime import datetime
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../")))

from main import app, db
from models import Transaction, Budget, Category
from observers.budget_observer import BudgetObserver
from testing.base_test_case import BaseTestCase


class TestBudgetObserver(BaseTestCase):
    def setUp(self):
        super().setUp()
        test_category = Category(name="Test Category", type="expense")
        db.session.add(test_category)
        db.session.commit()
        self.category_id = test_category.id
        
        test_budget = Budget(
            category_id=self.category_id,
            amount=1000.0,
            month="April 2025",
            spent_amount=0.0
        )
        db.session.add(test_budget)
        db.session.commit()
        self.test_budget_id = test_budget.id
    
    def test_update_budget_on_transaction_creation(self):
        # This creates a transaction without saving it to the database then calls Budget Observer
        transaction = Transaction(
            amount=200.0,
            description="Test transaction",
            date=datetime.now(),
            type="expense",
            budget_id=self.test_budget_id
        )
        BudgetObserver.update_budget_on_transaction_update(transaction)
        
        # This checks if the budget was updated correctly by the observer
        updated_budget = Budget.query.get(self.test_budget_id)
        self.assertEqual(updated_budget.spent_amount, 200.0)
    
    def test_update_budget_on_transaction_update(self):
        transaction = Transaction(
            amount=300.0,
            description="Test transaction",
            date=datetime.now(),
            type="expense",
            budget_id=self.test_budget_id
        )
        transaction.save_to_db()
        
        budget_after_creation = Budget.query.get(self.test_budget_id)
        self.assertEqual(budget_after_creation.spent_amount, 300.0)
        
        transaction.amount = 500.0
        BudgetObserver.update_budget_on_transaction_update(transaction, old_amount=300.0)
        
        updated_budget = Budget.query.get(self.test_budget_id)
        self.assertEqual(updated_budget.spent_amount, 500.0)
    
    def test_update_budget_on_transaction_delete(self):
        transaction = Transaction(
            amount=150.0,
            description="Test transaction",
            date=datetime.now(),
            type="expense",
            budget_id=self.test_budget_id
        )
        transaction.save_to_db()
        
        budget_after_creation = Budget.query.get(self.test_budget_id)
        self.assertEqual(budget_after_creation.spent_amount, 150.0)
        
        old_amount = transaction.amount
        transaction.amount = 0.0
        
        # This simulates deletion by calling the observer with old_amount and setting it to 0
        BudgetObserver.update_budget_on_transaction_update(transaction, old_amount=old_amount)
        
        # This checks if the budget was updated correctly
        updated_budget = Budget.query.get(self.test_budget_id)
        self.assertEqual(updated_budget.spent_amount, 0.0)
        
    def test_update_budget_handles_negative_amounts(self):
        transaction = Transaction(
            amount=100.0,
            description="Test transaction",
            date=datetime.now(),
            type="expense",
            budget_id=self.test_budget_id
        )
        transaction.save_to_db()
        
        # This tries to update with an amount that would cause a negative spent_amount
        BudgetObserver.update_budget_on_transaction_update(transaction, old_amount=200.0)
        
        # This checks if the budget handles it correctly (it shouldn't go below 0)
        updated_budget = Budget.query.get(self.test_budget_id)
        self.assertEqual(updated_budget.spent_amount, 0.0)


if __name__ == "__main__":
    unittest.main()
    