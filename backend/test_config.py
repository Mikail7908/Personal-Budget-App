# test_config.py or a separate file like base_test_case.py

from main import app
from extensions import db  # Import db object from extensions
import unittest

def create_test_app():
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"  # Use in-memory SQLite for testing
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False  # Optional but recommended
    app.config["SECRET_KEY"] = "test-secret-key"  # Optional but good practice
    
    return app

class BaseTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Sets up the app context before any tests are run."""
        cls.app = create_test_app()  # Create the app using the function
        cls.client = cls.app.test_client()  # Get the test client
        cls.app_context = cls.app.app_context()  # Get app context
        cls.app_context.push()  # Push app context
        
        with cls.app.app_context():
            db.create_all()  # Create all database tables
    
    @classmethod
    def tearDownClass(cls):
        """Cleans up after tests have run."""
        with cls.app.app_context():
            db.session.remove()  # Remove the session
            db.drop_all()  # Drop all database tables
        cls.app_context.pop()  # Pop the app context
    
    # Now you can create other helper methods if needed for the tests

# You can now import and inherit from BaseTestCase in your actual test files.
