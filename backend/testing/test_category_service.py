import os
import sys
import unittest
from datetime import datetime

# Adjusting path so imports work correctly
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../")))

from test_config import create_test_app
from extensions import db
from models import Category
from services.category_service import CategoryService

class TestCategoryService(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Sets up the app and database before any tests are run."""
        cls.app = create_test_app()  # Use the helper function to create the test app
        cls.app_context = cls.app.app_context()  # Get the app context
        cls.app_context.push()  # Push the app context

        with cls.app.app_context():
            db.create_all()  # Create all the tables for testing

            # Create a test category to be used in tests
            test_category = Category(name="Test Category", type="expense")
            db.session.add(test_category)
            db.session.commit()
            cls.test_category_id = test_category.id

    @classmethod
    def tearDownClass(cls):
        """Cleans up after all tests have run."""
        with cls.app.app_context():
            db.session.remove()  # Clean up session
            db.drop_all()  # Drop all tables
        cls.app_context.pop()  # Pop the app context

    def test_create_category(self):
        test_new_category_data = {
            "name": "New Test Category",
            "type": "income"
        }

        with self.app.app_context():
            result = CategoryService.create_category(test_new_category_data)
            self.assertIsNotNone(result)
            self.assertEqual(result.name, "New Test Category")
            self.assertEqual(result.type, "income")
            saved_category = Category.query.filter_by(name="New Test Category").first()
            self.assertIsNotNone(saved_category)

    def test_get_all_categories(self):
        with self.app.app_context():
            categories = CategoryService.get_all_categories()
            self.assertEqual(len(categories), 1)
            self.assertEqual(categories[0]["name"], "Test Category")
            self.assertEqual(categories[0]["type"], "expense")

    def test_update_category(self):
        update_data = {
            "name": "Updated Category Name",
            "type": "income"
        }

        with self.app.app_context():
            result = CategoryService.update_category(self.test_category_id, update_data)
            self.assertIsNotNone(result)
            self.assertEqual(result.name, "Updated Category Name")
            self.assertEqual(result.type, "income")
            updated_category = Category.query.get_or_404(self.test_category_id)
            self.assertEqual(updated_category.name, "Updated Category Name")
            self.assertEqual(updated_category.type, "income")

    def test_delete_category(self):
        with self.app.app_context():
            initial_category_count = len(Category.query.all())
            CategoryService.delete_category(self.test_category_id)
            self.assertEqual(len(Category.query.all()), initial_category_count - 1)
            self.assertIsNone(Category.query.get(self.test_category_id))


if __name__ == "__main__":
    unittest.main()
