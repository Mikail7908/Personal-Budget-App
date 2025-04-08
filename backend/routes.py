from main import app
from flask import *
from models import Transaction, Budget
from datetime import *

@app.route("/transactions", methods=["POST"])
def create_transaction():
    transaction_data = request.json()
    new_transaction = Transaction(
        amount=transaction_data["amount"],
        description=transaction_data["description"],
        date=datetime.strptime(transaction_data["date"], "%Y-%m-%d")
    )
    new_transaction.save_to_db()
    return jsonify({
        "message": "Successfully created new transaction",
        "transaction_id": new_transaction.id
    }), 201

@app.route("/transactions", methods=["GET"])
def view_all_transactions():
    all_transactions = Transaction.fetch_all()
    transaction_list = [{
        "transaction_id": transaction.id,
        "amount": transaction.amount,
        "description": transaction.description,
        "date": transaction.date.strftime("%Y-%m-%d")
    } for transaction in all_transactions]
    return jsonify(transaction_list), 200

@app.route("/transactions/<int:id>", methods=["PUT"])
def edit_transaction(transaction_id):
    transaction_data = request.json
    updated_transaction = Transaction.update(transaction_id, transaction_data)
    return jsonify({
        "message": "Successfully updated transaction",
        "transaction_id": updated_transaction.id
    }), 200

@app.route("/transactions/<int:id>", methods=["DELETE"])
def delete_transaction(transaction_id):
    Transaction.delete(transaction_id)
    return jsonify({"message": "Transaction deleted successfully"}), 200
    
@app.route("/budget-goals", methods=["POST"])
def create_budget_goal():
    pass

@app.route("/budget-goals", methods=["POST"])
def view_all_budget_goals():
    pass

@app.route("/budget-goals/<int:id>", methods=["PUT"])
def edit_budget_goal(id):
    pass

@app.route("/budget-goals/<int:id>", methods=["DELETE"])
def delete_budget_goal(id):
    pass