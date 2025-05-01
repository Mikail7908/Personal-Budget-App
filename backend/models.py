from datetime import datetime
from backend.extensions import db
from sqlalchemy.orm import relationship
from backend.observers.budget_observer import BudgetObserver

class BaseModel(db.Model):
    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    date = db.Column(db.DateTime, nullable=False, default=datetime.now)

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def fetch_all(cls):
        return cls.query.order_by(cls.date.desc()).all()

    @classmethod
    def delete(cls, id):
        item = cls.query.get_or_404(id)
        db.session.delete(item)
        db.session.commit()

# Transaction with budget-aware sync
class Transaction(BaseModel):
    __tablename__ = "transactions"

    amount = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(255), nullable=False)
    type = db.Column(db.String(50), nullable=False)  
    budget_id = db.Column(db.Integer, db.ForeignKey("budgets.id"), nullable=True)
    savings_goal_id = db.Column(db.Integer, db.ForeignKey("savings_goals.id"), nullable=True)  
    budget = relationship("Budget", back_populates="transactions")
    savings_goal = relationship("SavingsGoal", backref="transactions", lazy=True) 
    def validate_amount(self):
        if self.amount <= 0:
            raise ValueError("Amount must be greater than 0")

    def save_to_db(self, old_amount=None):
        BaseModel.save_to_db(self)
        BudgetObserver.update_budget_on_transaction_update(
            self,
            old_amount=old_amount,
            new_amount=self.amount
        )
        # old_amount = None
        # if self.id and old_amount is None:
        #     old_transaction = Transaction.query.get(self.id)
        #     old_amount = old_transaction.amount if old_transaction else None
            
        # BaseModel.save_to_db(self)
        # BudgetObserver.update_budget_on_transaction_update(self, old_amount=old_amount, new_amount=self.amount)
        
    def delete_from_db(self):
        old_amount = self.amount
        BudgetObserver.update_budget_on_transaction_update(self, old_amount)
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        return f"<Transaction {self.id}: {self.description} - {self.amount}>"


class Category(BaseModel):
    __tablename__ = "categories"

    name = db.Column(db.String(255), nullable=False)
    type = db.Column(db.String(255), nullable=False) 

    @staticmethod
    def update(category_id, category_data):
        category = Category.query.get_or_404(category_id)
        category.name = category_data["name"]
        category.type = category_data["type"]
        db.session.commit()
        return category

    budgets = relationship("Budget", back_populates="category")

class Budget(BaseModel):
    __tablename__ = "budgets"

    category_id = db.Column(db.Integer, db.ForeignKey("categories.id"), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    month = db.Column(db.String(20), nullable=False)
    spent_amount = db.Column(db.Float, default=0.00)

    category = relationship("Category", back_populates="budgets")
    transactions = relationship("Transaction", back_populates="budget")

    def calculate_remaining(self):
        return self.amount - self.spent_amount

    @staticmethod
    def update(budget_id, budget_data):
        budget = Budget.query.get_or_404(budget_id)
        budget.amount = budget_data["amount"]
        budget.month = budget_data["month"]
        db.session.commit()
        return budget


class SavingsGoal(BaseModel):
    __tablename__ = "savings_goals"

    target_amount = db.Column(db.Float, nullable=False)
    current_amount = db.Column(db.Float, default=0.00, nullable=False)
    deadline = db.Column(db.DateTime, nullable=False)
    description = db.Column(db.String(255), nullable=False)
    saving_frequency = db.Column(db.String(50), nullable=False)

    def calculate_progress(self):
        return (self.current_amount / self.target_amount) * 100 if self.target_amount else 0

    @staticmethod
    def update(savings_goal_id, savings_goal_data):
        savings_goal = SavingsGoal.query.get_or_404(savings_goal_id)
        savings_goal.target_amount = float(savings_goal_data["target_amount"])
        savings_goal.current_amount = float(savings_goal_data["current_amount"])
        savings_goal.deadline = datetime.strptime(savings_goal_data["deadline"], "%Y-%m-%d")
        savings_goal.description = savings_goal_data["description"]
        savings_goal.saving_frequency = savings_goal_data["saving_frequency"]
        db.session.commit()
        return savings_goal

    def __repr__(self):
        return f"<SavingsGoal {self.id}: {self.description} - Progress: {self.calculate_progress():.1f}%>"
