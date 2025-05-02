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
    @classmethod
    def setUpClass(cls):
        """Sets up the app and database before any tests are run."""
        cls.app = create_test_app()  # Use the helper function to create the test app
        cls.app_context = cls.app.app_context()  # Get the app context
        cls.app_context.push()  # Push the app context

        with cls.app.app_context():
            db.create_all()  # Create all the tables for testing

    @classmethod
    def tearDownClass(cls):
        """Cleans up after all tests have run."""
        with cls.app.app_context():
            db.session.remove()  # Clean up session
            db.drop_all()  # Drop all tables
        cls.app_context.pop()  # Pop the app context

    def test_transaction_creation(self):
        with self.app.app_context():
            test_transaction = Transaction(
                amount=100.0,
                description="Test",
                type="expense",
                date=datetime.now(),
            )
            test_transaction.save_to_db()  # Save transaction to DB
            transaction = Transaction.query.first()  # Fetch the first transaction
            self.assertIsNotNone(transaction)  # Ensure the transaction exists in DB
            self.assertEqual(transaction.amount, 100.0)
            self.assertEqual(transaction.description, "Test")
            self.assertEqual(transaction.type, "expense")

if __name__ == "__main__":
    unittest.main()
