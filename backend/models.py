from datetime import datetime
from extensions import db 
from sqlalchemy.orm import relationship

class Transaction(db.Model):
    __tablename__ = "transactions"

    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    amount = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(255), nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    type = db.Column(db.String(50), nullable=False)  # income or expense

    def validate_amount(self):
        if self.amount <= 0:
            raise ValueError("Amount must be greater than 0")

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def fetch_all():
        return Transaction.query.order_by(Transaction.date.desc()).all()

    @staticmethod
    def update(transaction_id, transaction_data):
        transaction = Transaction.query.get_or_404(transaction_id)
        transaction.amount = transaction_data["amount"]
        transaction.description = transaction_data["description"]
        transaction.date = datetime.strptime(transaction_data["date"], "%Y-%m-%d")
        transaction.type = transaction_data["type"]
        db.session.commit()
        return transaction

    @staticmethod
    def delete(transaction_id):
        transaction = Transaction.query.get_or_404(transaction_id)
        db.session.delete(transaction)
        db.session.commit()

    def __repr__(self):
        return f"<Transaction {self.id}: {self.description} - {self.amount}>"

class Category(db.Model):
    __tablename__ = "categories"

    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    name = db.Column(db.String(255), nullable=False)
    type = db.Column(db.String(255), nullable=False)  # e.g., "expense", "income"

    budgets = relationship("Budget", back_populates="category")

class Budget(db.Model):
    __tablename__ = "budgets"

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
    __tablename__ = "savings_goals"

    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    target_amount = db.Column(db.Float, nullable=False)
    current_amount = db.Column(db.Float, default=0.00, nullable=False)
    deadline = db.Column(db.DateTime, nullable=False)
    description = db.Column(db.String(255), nullable=False)
    saving_frequency = db.Column(db.String(50), nullable=False)

    def calculate_progress(self):
        return (self.current_amount / self.target_amount) * 100 if self.target_amount else 0

    def __repr__(self):
        return f"<SavingsGoal {self.id}: {self.description} - Progress: {self.calculate_progress():.1f}%>"
