# routes.py
from flask import Blueprint, request, jsonify
from models import Transaction, Budget, Category
from datetime import datetime

api = Blueprint("api", __name__)


@api.route("/api/test", methods=["GET"])
def test():
    return jsonify({"message": "Test route working ✅"})

#Transaction Routes
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

#Budget Routes
@api.route("/api/budget", methods=["POST"])
def create_budget():
    budget_data = request.json()
    new_budget = Budget(
        category_id=budget_data["category_id"],
        amount=budget_data["amount"],
        month=budget_data["month"]
    )
    new_budget.save_to_db()
    return jsonify({
        "message": "Successfully created new budget",
        "budget_id": new_budget.id
    }), 201

@api.route("/api/budget", methods=["POST"])
def view_all_budget():
    all_budgets = Budget.fetch_all()
    budget_list = [{
        "budget_id": budget.id,
        "category_id": budget.category_id,
        "amount": budget.amount,
        "month": budget.month
    } for budget in all_budgets]
    return jsonify(budget_list), 200

@api.route("/api/budget/<int:id>", methods=["PUT"])
def edit_budget(budget_id):
    budget_data = request.json
    updated_budget = Budget.update(budget_id, budget_data)
    return jsonify({
        "message": "Successfully updated budget",
        "budget_id": updated_budget.id
    }), 200

@api.route("/api/budget/<int:id>", methods=["DELETE"])
def delete_budget(budget_id):
    Budget.delete(budget_id)
    return jsonify({"message": "Budget deleted successfully"}), 200

#Catagory Routes
@api.route("/api/categories", methods=["GET"])
def create_category():
    category_data = request.json()
    new_category = Category(
        name=category_data["name"],
        type=category_data["type"]
    )
    new_category.save_to_db()
    return jsonify({
        "message": "Successfully created new category",
        "category_id": new_category.id
    }), 201

def view_all_categories():
    all_categories = Category.fetch_all()
    category_list = [{
        "category_id": category.id,
        "name": category.name,
        "type": category.type
    } for category in all_categories]
    return jsonify(category_list), 200

def edit_category(category_id):
    category_data = request.json()
    updated_category = Category.update(category_id, category_data)
    return jsonify({
        "message": "Successfully updated category",
        "category_id": updated_category.id
    }), 200

def delete_category(category_id):
    Category.delete(category_id)
    return jsonify({"message": "Category deleted successfully"}), 200
