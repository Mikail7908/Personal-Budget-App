# routes.py
from flask import Blueprint, request, jsonify
from models import Transaction
from datetime import datetime

api = Blueprint("api", __name__)


@api.route("/api/test", methods=["GET"])
def test():
    return jsonify({"message": "Test route working ✅"})

@api.route("/api/transactions", methods=["POST"])
def create_transaction():
    data = request.get_json()
    new_transaction = Transaction(
        amount=data["amount"],
        description=data["description"],
        date=datetime.strptime(data["date"], "%Y-%m-%d"),
        type=data["type"]
    )
    new_transaction.save_to_db()
    return jsonify({"message": "Created", "id": new_transaction.id}), 201


@api.route("/api/transactions", methods=["GET"])
def view_all_transactions():
    all_transactions = Transaction.fetch_all()
    transaction_list = [{
        "id": transaction.id,
        "amount": transaction.amount,
        "description": transaction.description,
        "date": transaction.date.strftime("%Y-%m-%d"),
        "type": transaction.type
    } for transaction in all_transactions]
    return jsonify(transaction_list), 200

@api.route("/api/transactions/<int:id>", methods=["PUT"])
def edit_transaction(id):
    transaction_data = request.get_json()
    updated_transaction = Transaction.update(id, transaction_data)
    return jsonify({
        "message": "Successfully updated transaction",
        "id": updated_transaction.id
    }), 200

@api.route("/api/transactions/<int:id>", methods=["DELETE"])
def delete_transaction(id):
    Transaction.delete(id)
    return jsonify({"message": "Transaction deleted successfully"}), 200

# Budget goals placeholder endpoints
@api.route("/budget-goals", methods=["POST"])
def create_budget_goal():
    return jsonify({"message": "Not implemented"}), 501

@api.route("/budget-goals", methods=["GET"])  # ✅ FIXED: changed to GET
def view_all_budget_goals():
    return jsonify({"message": "Not implemented"}), 501

@api.route("/budget-goals/<int:id>", methods=["PUT"])
def edit_budget_goal(id):
    return jsonify({"message": "Not implemented"}), 501

@api.route("/budget-goals/<int:id>", methods=["DELETE"])
def delete_budget_goal(id):
    return jsonify({"message": "Not implemented"}), 501
