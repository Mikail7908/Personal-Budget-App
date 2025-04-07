from main import app
from flask import *

@app.route("/", methods=["POST"])
def home():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        return 'Logged in currently'
        

@app.route("/transactions", methods=["POST"])
def create_transaction():
    pass

@app.route("/transactions", methods=["GET"])
def view_all_transactions():
    pass

@app.route("/transactions/<int:id>", methods=["PUT"])
def edit_transaction(id):
    pass

@app.route("/transactions/<int:id>", methods=["DELETE"])
def delete_transaction(id):
    pass
    
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