import sys
import os
import unittest
from datetime import datetime

# Adjusting path so imports work correctly
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../")))

from test_config import create_test_app
from models import Transaction, Budget, SavingsGoal, Category
from extensions import db  # Import the db object from extensions

class TestModels(unittest.TestCase):
    def setUp(self):
        # Use the helper function from test_config to set up the test app
        self.app = create_test_app()
        self.app_context = self.app.app_context()
        self.app_context.push()
        
        with self.app.app_context():
            db.create_all()  # Create all the tables

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()  # Clean up session
            db.drop_all()  # Drop all tables after test
    
    def test_transaction_creation(self):
        with self.app.app_context():
            test_transaction = Transaction(
                amount=100.0,
                description="Test",
                type="expense",
                date=datetime.now(),
            )
            test_transaction.save_to_db()
            transaction = Transaction.query.first()
            self.assertIsNotNone(transaction)
            self.assertEqual(transaction.amount, 100.0)
            self.assertEqual(transaction.description, "Test")
            self.assertEqual(transaction.type, "expense")

if __name__ == "__main__":
    unittest.main()
