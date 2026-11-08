from database import get_connection
from models.category import Category


class CategoryRepository:

    # Добавление категории
    def add(self, name, description):
        connection = get_connection()

        connection.execute(
            "INSERT INTO categories (name, description) VALUES (?, ?)",
            (name, description)
        )

        connection.commit()
        connection.close()

    # Поиск категории по ID
    def get_by_id(self, category_id):
        connection = get_connection()

        row = connection.execute(
            "SELECT * FROM categories WHERE id = ?",
            (category_id,)
        ).fetchone()

        connection.close()

        if row is None:
            return None

        return Category(*row)

    # Получение всех категорий
    def get_all(self):
        connection = get_connection()

        rows = connection.execute(
            "SELECT * FROM categories"
        ).fetchall()

        connection.close()

        return [Category(*row) for row in rows]

    # Изменение категории
    def update(self, category_id, name, description):
        connection = get_connection()

        connection.execute(
            "UPDATE categories SET name = ?, description = ? WHERE id = ?",
            (name, description, category_id)
        )

        connection.commit()
        connection.close()

    # Удаление категории
    def delete(self, category_id):
        connection = get_connection()

        connection.execute(
            "DELETE FROM categories WHERE id = ?",
            (category_id,)
        )

        connection.commit()
        connection.close()