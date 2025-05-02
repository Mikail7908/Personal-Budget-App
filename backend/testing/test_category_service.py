import os
import sys
import unittest

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../")))

from main import app, db
from models import Category
from services.category_service import CategoryService
from testing.base_test_case import BaseTestCase


class TestCategoryService(BaseTestCase):
    def setUp(self):
        super().setUp()
        test_category = Category(name="Test Category", type="expense")
        db.session.add(test_category)
        db.session.commit()
        self.test_category_id = test_category.id

    def test_create_category(self):
        test_new_category_data = {"name": "New Test Category", "type": "income"}

        result = CategoryService.create_category(test_new_category_data)
        self.assertIsNotNone(result)
        self.assertEqual(result.name, "New Test Category")
        self.assertEqual(result.type, "income")
        saved_category = Category.query.filter_by(name="New Test Category").first()
        self.assertIsNotNone(saved_category)

    def test_get_all_categories(self):
        categories = CategoryService.get_all_categories()
        self.assertEqual(len(categories), 1)
        self.assertEqual(categories[0]["name"], "Test Category")
        self.assertEqual(categories[0]["type"], "expense")

    def test_update_category(self):
        update_data = {"name": "Updated Category Name", "type": "income"}

        result = CategoryService.update_category(self.test_category_id, update_data)
        self.assertIsNotNone(result)
        self.assertEqual(result.name, "Updated Category Name")
        self.assertEqual(result.type, "income")
        updated_category = Category.query.get_or_404(self.test_category_id)
        self.assertEqual(updated_category.name, "Updated Category Name")
        self.assertEqual(updated_category.type, "income")

    def test_delete_category(self):
        initial_category_count = len(Category.query.all())
        CategoryService.delete_category(self.test_category_id)
        self.assertEqual(len(Category.query.all()), initial_category_count - 1)
        self.assertIsNone(Category.query.get(self.test_category_id))


if __name__ == "__main__":
    unittest.main()