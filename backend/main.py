from flask import Flask
from flask_migrate import Migrate
from flask_cors import CORS
from extensions import db
import os

app = Flask(__name__)
app.config["SECRET_KEY"] = "super-secret"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///budget_database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Set CORS based on the environment
if os.environ.get("FLASK_ENV") == "production":
    CORS(app, resources={r"/api/*": {"origins": "https://your-frontend-url.com"}})
else:
    CORS(app, resources={r"/api/*": {"origins": "http://localhost:5173"}})

db.init_app(app)
migrate = Migrate(app, db)

# Import routes *after* app + db setup
from routes import api
app.register_blueprint(api)

with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)
