import sys
import os
import unittest
from datetime import datetime
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../")))

from main import app, db
from models import Transaction
from services.transaction_service import TransactionService


class TestTransactionValidation(unittest.TestCase):
    def setUp(self):
        app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
        app.config["TESTING"] = True
        self.app_context = app.app_context()
        self.app_context.push()
        db.create_all()
    
    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()
    
    def test_negative_amount_validation(self):
        # This checks the error handling of the class itself
        transaction = Transaction(
            amount=-100.0,
            description="Negative amount",
            date=datetime.now(),
            type="expense"
        )
        with self.assertRaises(ValueError):
            transaction.validate_amount()
        
        # This checks the error handling of the transaction service
        invalid_data = {
            "amount": "-50.0",
            "description": "Test negative amount",
            "date": "2025-05-01",
            "type": "expense"
        }
        with self.assertRaises(Exception):
            TransactionService.create_transaction(invalid_data)
    
    def test_zero_amount_validation(self):
        # This checks the error handling of the class itself
        transaction = Transaction(
            amount=0.0,
            description="Zero amount",
            date=datetime.now(),
            type="expense"
        )
        with self.assertRaises(ValueError):
            transaction.validate_amount()
            
        # This checks the error handling of the transaction service
        invalid_data = {
            "amount": "0.0",
            "description": "Test zero amount",
            "date": "2025-05-01",
            "type": "expense"
        }
        with self.assertRaises(Exception):
            TransactionService.create_transaction(invalid_data)
            
            
if __name__ == "__main__":
    unittest.main()
    