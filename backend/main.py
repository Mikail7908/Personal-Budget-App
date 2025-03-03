from flask import Flask
from flask_cors import CORS
import sqlite3

app = Flask(__name__)
CORS(app)


if __name__ == "__main__":
    app.run(debug=True)