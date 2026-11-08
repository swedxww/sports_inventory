import sqlite3
from repositories.category_repository import CategoryRepository


class CategoryService:

    def __init__(self):
        self.repository = CategoryRepository()

    # Проверка прав администратора
    def check_admin(self, user):
        if user is None or user.role != "admin":
            raise PermissionError("Недостаточно прав для выполнения операции")

    # Добавление категории
    def add_category(self, user, name, description):
        self.check_admin(user)

        if not name.strip():
            raise ValueError("Название категории не может быть пустым")

        try:
            self.repository.add(name.strip(), description)
        except sqlite3.IntegrityError:
            raise ValueError("Такая категория уже существует")

    # Получение всех категорий
    def get_all_categories(self):
        return self.repository.get_all()

    # Поиск категории по ID
    def get_category(self, category_id):
        category = self.repository.get_by_id(category_id)

        if category is None:
            raise ValueError("Категория не найдена")

        return category

    # Изменение категории
    def update_category(self, user, category_id, name, description):
        self.check_admin(user)
        self.get_category(category_id)

        if not name.strip():
            raise ValueError("Название категории не может быть пустым")

        try:
            self.repository.update(category_id, name.strip(), description)
        except sqlite3.IntegrityError:
            raise ValueError("Такая категория уже существует")

    # Удаление категории
    def delete_category(self, user, category_id):
        self.check_admin(user)
        self.get_category(category_id)

        try:
            self.repository.delete(category_id)
        except sqlite3.IntegrityError:
            raise ValueError("Нельзя удалить категорию, в которой есть инвентарь")