import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../")))

import unittest
from datetime import datetime
from backend.main import app, db
from backend.models import Transaction, Budget, SavingsGoal, Category

# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../")))
print("SYSTEM PATH", sys.path)

class TestModels(unittest.TestCase):
    def set_up_database(self):
        app.config["SQLALCHEMY_DATABASE_URI"]
        app.config["TESTING"] = True
        self.app = app.test_client()
        with app.app_context():
            db.create_all()
    
    def tear_down_database(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()
            
    def test_transaction_creation(self):
        with app.app_context():
            test_transaction = Transaction(
                amount=100.0,
                description="Test",
                type="expense",
                date=datetime.now,
            )
            test_transaction.save_to_db()
            transaction = Transaction.query.first()
            self.assertIsNotNone(transaction)
            self.assertEqual(transaction.amount, 100.0)
            self.assertEqual(transaction.description, "Test")
            self.assertEqual(transaction.type, "expense")
            
if __name__ == "__main__":
    unittest.main()