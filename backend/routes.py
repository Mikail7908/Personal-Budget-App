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
    