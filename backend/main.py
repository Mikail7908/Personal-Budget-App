from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import sqlite3

# class that returns database connection. have to create cursor when calling this class
class DatabaseManager:
    def __init__(self, db_name):
        self.db_name = db_name

    def create_connection(self):
        conn = sqlite3.connect(self.db_name)
        return conn



app = Flask(__name__)
app.config["SECRET_KEY"] = "78af91b1d81e440cbe0059d259d52745"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///budget_database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
CORS(app)

db = SQLAlchemy(app)

if __name__ == "__main__":
    app.run(debug=True)