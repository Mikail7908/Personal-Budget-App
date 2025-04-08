from datetime import datetime
from main import db
from sqlalchemy import *
from sqlalchemy.orm import *
import sqlite3
    
    
class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, default=datetime.now(), onupdate=datetime.now())
    amount = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(255), nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    
    def validate_amount(self) -> None:
        if self.amount <= 0:
            raise ValueError("Amount must be greater than 0")
        
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
        
    def fetch_all():
        return Transaction.query.all()
    
    def update(transaction_id, transaction_data):
        transaction = Transaction.query.get_or_404(transaction_id)
        transaction.amount = transaction_data["amount"]
        transaction.description = transaction_data["description"]
        transaction.date = datetime.strptime(transaction_data["date"], "%Y-%m-%d")
        db.session.commit()
        return transaction
    
    def delete(transaction_id):
        transaction = Transaction.query.get_or_404(transaction_id)
        db.session.delete(transaction)
        db.session.commit()


class Income(Transaction):
    id = db.Column(db.Integer, primary_key=True)
    source = db.Column(db.String(255), nullable=False)
    frequency = db.Column(db.String(255), nullable=False)
        
         
class Expense(Transaction):
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(255), nullable=False)
    payment_method = db.Column(db.String(255), nullable=False)
        

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, default=datetime.now(), onupdate=datetime.now())
    name = db.Column(db.String(255), nullable=False)
    type = db.Column(db.String(255), nullable=False)
    
    budgets = relationship("Budget", back_populates="category")
    
    
class Budget(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    category_id = db.Column(db.Integer, db.ForeignKey("categories.id"), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    month = db.Column(db.String(20), nullable=False)
    spent_amount = db.Column(db.Float, default=0.00)
    category = relationship("Category", back_populates="budgets")
        
    def calculate_remaining(self):
        return self.amount - self.spent_amount
    
    def update_spent_amount(self, amount):
        self.spent_amount += amount
        db.session.commit()

class SavingsGoal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    target_amount = db.Column(db.Float, nullable=False)
    current_amount = db.Column(db.Float, default=0.00, nullable=False)
    deadline = db.Column(db.DateTime, nullable=False)
    description = db.Column(db.String(255), nullable=False)
    saving_frequency = db.Column(db.String(50), nullable=False)
        
    def calculate_progress(self):
        return (self.current_amount / self.target_amount) * 100
    
    def project_completion_date(self):
        pass
    