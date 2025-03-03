from flask import Flask
from flask_cors import CORS
import sqlite3

# class that returns database connection. have to create cursor when calling this class
class DatabaseManager:
    def __init__(self, db_name):
        self.db_name = db_name

    def create_connection(self):
        conn = sqlite3.connect(self.db_name)
        return conn



app = Flask(__name__)
CORS(app)


if __name__ == "__main__":
    app.run(debug=True)