from database import get_connection
from models.equipment import Equipment


class EquipmentRepository:

    # Добавление инвентаря
    def add(self, name, quantity, condition, category_id):
        connection = get_connection()

        connection.execute(
            """
            INSERT INTO equipment (name, quantity, condition, category_id)
            VALUES (?, ?, ?, ?)
            """,
            (name, quantity, condition, category_id)
        )

        connection.commit()
        connection.close()

    # Поиск инвентаря по ID
    def get_by_id(self, equipment_id):
        connection = get_connection()

        row = connection.execute(
            "SELECT * FROM equipment WHERE id = ?",
            (equipment_id,)
        ).fetchone()

        connection.close()

        if row is None:
            return None

        return Equipment(*row)

    # Получение всего инвентаря
    def get_all(self):
        connection = get_connection()

        rows = connection.execute(
            "SELECT * FROM equipment"
        ).fetchall()

        connection.close()

        return [Equipment(*row) for row in rows]

    # Изменение инвентаря
    def update(self, equipment_id, name, quantity, condition, category_id):
        connection = get_connection()

        connection.execute(
            """
            UPDATE equipment
            SET name = ?, quantity = ?, condition = ?, category_id = ?
            WHERE id = ?
            """,
            (name, quantity, condition, category_id, equipment_id)
        )

        connection.commit()
        connection.close()

    # Удаление инвентаря
    def delete(self, equipment_id):
        connection = get_connection()

        connection.execute(
            "DELETE FROM equipment WHERE id = ?",
            (equipment_id,)
        )

        connection.commit()
        connection.close()