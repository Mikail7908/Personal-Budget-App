# routes.py
from flask import Blueprint, request, jsonify
from models import Transaction, Budget, Category, SavingsGoal
from datetime import datetime

api = Blueprint("api", __name__)

@api.route("/api/test", methods=["GET"])
def test():
    return jsonify({"message": "Test route working ✅"})

# Transaction Routes
@api.route("/api/transactions", methods=["POST"])
def create_transaction():
    try:
        data = request.get_json()
        new_transaction = Transaction(
            amount=float(data["amount"]),
            description=data["description"],
            date=datetime.strptime(data["date"], "%Y-%m-%d"),
            type=data["type"],
            budget_id=data.get("budget_id")
        )
        new_transaction.validate_amount()
        new_transaction.save_to_db()
        return jsonify({"message": "Created", "id": new_transaction.id}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@api.route("/api/transactions", methods=["GET"])
def view_all_transactions():
    all_transactions = Transaction.fetch_all()
    transaction_list = [{
        "id": transaction.id,
        "amount": transaction.amount,
        "description": transaction.description,
        "date": transaction.date.strftime("%Y-%m-%d"),
        "type": transaction.type,
        "budget_id": transaction.budget_id
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

# Budget Routes
@api.route("/api/budgets", methods=["POST"])
def create_budget():
    try:
        budget_data = request.get_json()
        new_budget = Budget(
            category_id=budget_data["category_id"],
            amount=float(budget_data["amount"]),
            month=budget_data["month"]
        )
        new_budget.save_to_db()
        return jsonify({
            "message": "Successfully created new budget",
            "budget_id": new_budget.id
        }), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@api.route("/api/budgets", methods=["GET"])
def view_all_budgets():
    all_budgets = Budget.fetch_all()
    budget_list = [{
        "id": budget.id,
        "category_id": budget.category_id,
        "amount": budget.amount,
        "month": budget.month,
        "spent_amount": budget.spent_amount,
        "remaining": budget.calculate_remaining()
    } for budget in all_budgets]
    return jsonify(budget_list), 200

@api.route("/api/budgets/<int:budget_id>", methods=["PUT"])
def edit_budget(budget_id):
    budget_data = request.get_json()
    updated_budget = Budget.update(budget_id, budget_data)
    return jsonify({
        "message": "Successfully updated budget",
        "budget_id": updated_budget.id
    }), 200

@api.route("/api/budgets/<int:budget_id>", methods=["DELETE"])
def delete_budget(budget_id):
    Budget.delete(budget_id)
    return jsonify({"message": "Budget deleted successfully"}), 200

# Category Routes
@api.route("/api/categories", methods=["POST"])
def create_category():
    try:
        category_data = request.get_json()
        new_category = Category(
            name=category_data["name"],
            type=category_data["type"]
        )
        new_category.save_to_db()
        return jsonify({
            "message": "Successfully created new category",
            "category_id": new_category.id
        }), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@api.route("/api/categories", methods=["GET"])
def view_all_categories():
    all_categories = Category.fetch_all()
    category_list = [{
        "id": category.id,
        "name": category.name,
        "type": category.type
    } for category in all_categories]
    return jsonify(category_list), 200

@api.route("/api/categories/<int:category_id>", methods=["PUT"])
def edit_category(category_id):
    category_data = request.get_json()
    updated_category = Category.update(category_id, category_data)
    return jsonify({
        "message": "Successfully updated category",
        "category_id": updated_category.id
    }), 200

@api.route("/api/categories/<int:category_id>", methods=["DELETE"])
def delete_category(category_id):
    Category.delete(category_id)
    return jsonify({"message": "Category deleted successfully"}), 200

# Savings Goal Routes
@api.route("/api/savings-goals", methods=["POST"])
def create_savings_goal():
    try:
        data = request.get_json()
        new_goal = SavingsGoal(
            target_amount=float(data["target_amount"]),
            current_amount=float(data.get("current_amount", 0)),
            deadline=datetime.strptime(data["deadline"], "%Y-%m-%d"),
            description=data["description"],
            saving_frequency=data["saving_frequency"]
        )
        new_goal.save_to_db()
        return jsonify({
            "message": "Successfully created new savings goal",
            "id": new_goal.id
        }), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@api.route("/api/savings-goals", methods=["GET"])
def view_all_savings_goals():
    all_goals = SavingsGoal.fetch_all()
    goals_list = [{
        "id": goal.id,
        "target_amount": goal.target_amount,
        "current_amount": goal.current_amount,
        "deadline": goal.deadline.strftime("%Y-%m-%d"),
        "description": goal.description,
        "saving_frequency": goal.saving_frequency,
        "progress": goal.calculate_progress()
    } for goal in all_goals]
    return jsonify(goals_list), 200

@api.route("/api/savings-goals/<int:goal_id>", methods=["PUT"])
def edit_savings_goal(goal_id):
    goal_data = request.get_json()
    updated_goal = SavingsGoal.update(goal_id, goal_data)
    return jsonify({
        "message": "Successfully updated savings goal",
        "id": updated_goal.id
    }), 200

@api.route("/api/savings-goals/<int:goal_id>", methods=["DELETE"])
def delete_savings_goal(goal_id):
    SavingsGoal.delete(goal_id)
    return jsonify({"message": "Savings goal deleted successfully"}), 200
