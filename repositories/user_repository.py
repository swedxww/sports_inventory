from database import get_connection
from models.user import User


class UserRepository:

    # Добавление пользователя
    def add(self, login, password_hash, role):
        connection = get_connection()

        connection.execute(
            """
            INSERT INTO users (login, password_hash, role)
            VALUES (?, ?, ?)
            """,
            (login, password_hash, role)
        )

        connection.commit()
        connection.close()

    # Поиск пользователя по логину
    def get_by_login(self, login):
        connection = get_connection()

        row = connection.execute(
            "SELECT * FROM users WHERE login = ?",
            (login,)
        ).fetchone()

        connection.close()

        if row is None:
            return None

        return User(*row)

    # Поиск пользователя по ID
    def get_by_id(self, user_id):
        connection = get_connection()

        row = connection.execute(
            "SELECT * FROM users WHERE id = ?",
            (user_id,)
        ).fetchone()

        connection.close()

        if row is None:
            return None

        return User(*row)

    # Получение всех пользователей
    def get_all(self):
        connection = get_connection()

        rows = connection.execute(
            "SELECT * FROM users"
        ).fetchall()

        connection.close()

        return [User(*row) for row in rows]

    # Изменение роли пользователя
    def update_role(self, user_id, role):
        connection = get_connection()

        connection.execute(
            "UPDATE users SET role = ? WHERE id = ?",
            (role, user_id)
        )

        connection.commit()
        connection.close()

    # Удаление пользователя
    def delete(self, user_id):
        connection = get_connection()

        connection.execute(
            "DELETE FROM users WHERE id = ?",
            (user_id,)
        )

        connection.commit()
        connection.close()