from flask import Flask
from flask_migrate import Migrate
from flask_cors import CORS
from extensions import db
import os


app = Flask(__name__)
app.config["SECRET_KEY"] = "super-secret"
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# This loads the frontend URL from environment or defaults to local dev environment
frontend_url = os.environ.get("FRONTEND_URL", "http://localhost:5173")

CORS(
    app,
    resources={
        r"/api/*": {
            "origins": frontend_url,
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            "allow_headers": ["Content-Type"],
        }
    },
)

db.init_app(app)
migrate = Migrate(app, db)

from routes import api

app.register_blueprint(api)

with app.app_context():
    db.create_all()


if __name__ == "__main__":
    app.run(debug=True, port=5001)
