from database import get_connection
from models.movement import Movement


class MovementRepository:

    # Добавление операции
    def add(self, equipment_id, movement_type, quantity, movement_date):
        connection = get_connection()

        connection.execute(
            """
            INSERT INTO equipment_movements
            (equipment_id, movement_type, quantity, movement_date)
            VALUES (?, ?, ?, ?)
            """,
            (equipment_id, movement_type, quantity, movement_date)
        )

        connection.commit()
        connection.close()

    # Поиск операции по ID
    def get_by_id(self, movement_id):
        connection = get_connection()

        row = connection.execute(
            "SELECT * FROM equipment_movements WHERE id = ?",
            (movement_id,)
        ).fetchone()

        connection.close()

        if row is None:
            return None

        return Movement(*row)

    # Получение всех операций
    def get_all(self):
        connection = get_connection()

        rows = connection.execute(
            "SELECT * FROM equipment_movements"
        ).fetchall()

        connection.close()

        return [Movement(*row) for row in rows]

    # Изменение операции
    def update(self, movement_id, equipment_id, movement_type,
               quantity, movement_date):
        connection = get_connection()

        connection.execute(
            """
            UPDATE equipment_movements
            SET equipment_id = ?, movement_type = ?,
                quantity = ?, movement_date = ?
            WHERE id = ?
            """,
            (equipment_id, movement_type, quantity,
             movement_date, movement_id)
        )

        connection.commit()
        connection.close()

    # Удаление операции
    def delete(self, movement_id):
        connection = get_connection()

        connection.execute(
            "DELETE FROM equipment_movements WHERE id = ?",
            (movement_id,)
        )

        connection.commit()
        connection.close()