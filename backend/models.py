from datetime import datetime

class BaseModel:
    def __init__(self, id=None, created_at=None, updated_at=None):
        self.id = id
        self.created_at = created_at or datetime.now()
        self.updated_at = updated_at or datetime.now()
        
    def save(self):
        print(f"Saving object {self.id}")
        
    def delete(self):
        print(f"Deleting obejct {self.id}")
        
    def get(self, id):
        print(f"Retrieving object {self.id}")
    
    
class Transaction(BaseModel):
    def __init__(self, amount: float, description: str, date: datetime, **kwargs):
        super().__init__(**kwargs)
        self.amount = amount
        self.description = description
        self.date = date
        
    def validate_amount(self) -> None:
        if self.amount <= 0:
            raise ValueError("Amount must be greater than 0")
        
    def process_transaction():
        pass
    

class Income(Transaction):
    def __init__(self, source, frequency, **kwargs):
        super().__init__(**kwargs)
        self.source = source
        self.frequency = frequency
        
    def validate_amount(self):
        pass
        
        
class Expense(Transaction):
    def __init__(self, category, payment_method, **kwargs):
        super().__init__(**kwargs)
        self.category = category
        self.payment_method = payment_method
        

class Category(BaseModel):
    def __init__(self, name, type, **kwargs):
        super().__init__(**kwargs)
        self.name = name
        self.type = type
    
    
class Budget(BaseModel):
    def __init__(self, category: Category, amount, month, spent_amount, **kwargs):
        super().__init__(**kwargs)
        self.category = category
        self.amount = amount
        self.month = month
        self.spent_amount = spent_amount
        
    def calculate_remaining(self):
        pass
    
    def update_spent_amount(self):
        pass
    

class SavingsGoal(BaseModel):
    def __init__(self, target_amount, current_amount, deadline: datetime, description, saving_frequency):
        self.target_amount = target_amount
        self.current_amount = current_amount
        self.deadline = deadline
        self.description = description
        self.saving_frequency = saving_frequency
        
    def calculate_progress(self):
        return (self.current_amount / self.target_amount) * 100
    
    def project_completion_date(self):
        pass