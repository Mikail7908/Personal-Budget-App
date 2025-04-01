from flask import Flask
from flask_cors import CORS
import sqlite3

class DatabaseManager:
    def __init__(self, db_name):
        self.db_name = db_name

    def create_connection(self):
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()


app = Flask(__name__)
app.config["SECRET_KEY"] = "78af91b1d81e440cbe0059d259d52745"
CORS(app)


if __name__ == "__main__":
    db = DatabaseManager("budget_database.db")
    app.run(debug=True)