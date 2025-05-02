from models import Category


class CategoryService:
    @staticmethod
    def create_category(data):
        try:
            new_category = Category(
                name=data["name"],
                type=data["type"]
            )
            new_category.save_to_db()
            return new_category
        except Exception as e:
            raise Exception(f"Error creating category: {str(e)}")
        
    @staticmethod
    def get_all_categories():
        try:
            all_categories = Category.fetch_all()
            category_list = [{
                "id": category.id,
                "name": category.name,
                "type": category.type
            } for category in all_categories]
            return category_list
        except Exception as e:
            raise Exception(f"Error fetching categories: {str(e)}")
        
    @staticmethod
    def update_category(category_id, data):
        try:
            category = Category.query.get_or_404(category_id)
            category.name = data["name"]
            category.type = data["type"]
            category.save_to_db()
            return category
        except Exception as e:
            raise Exception(f"Error updating category: {str(e)}")
        
    @staticmethod
    def delete_category(category_id):
        try:
            Category.delete(category_id)
        except Exception as e:
            raise Exception(f"Error deleting category: {str(e)}")
        