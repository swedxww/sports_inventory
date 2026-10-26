
import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent / "database" / "sports_inventory.db"
SCHEMA_PATH = Path(__file__).parent / "database" / "schema.sql"


def create_database():
    connection = sqlite3.connect(DB_PATH)

    with open(SCHEMA_PATH, "r", encoding="utf-8") as file:
        schema = file.read()

    connection.executescript(schema)

    connection.execute(
        "INSERT OR IGNORE INTO categories (name, description) VALUES (?, ?)",
        ("Мячи", "Спортивные мячи")
    )
    connection.execute(
        "INSERT OR IGNORE INTO categories (name, description) VALUES (?, ?)",
        ("Гантели", "Силовой инвентарь")
    )

    connection.execute(
        """INSERT INTO equipment (name, quantity, condition, category_id)
        SELECT 'Футбольный мяч', 10, 'Хорошее', id
        FROM categories WHERE name = 'Мячи'
        AND NOT EXISTS (
            SELECT 1 FROM equipment WHERE name = 'Футбольный мяч'
        )"""
    )
    connection.execute(
        """INSERT INTO equipment (name, quantity, condition, category_id)
        SELECT 'Гантели 5 кг', 8, 'Хорошее', id
        FROM categories WHERE name = 'Гантели'
        AND NOT EXISTS (
            SELECT 1 FROM equipment WHERE name = 'Гантели 5 кг'
        )"""
    )

    connection.execute(
        """INSERT INTO equipment_movements
        (equipment_id, movement_type, quantity, movement_date)
        SELECT id, 'Поступление', 10, '2026-10-26'
        FROM equipment WHERE name = 'Футбольный мяч'
        AND NOT EXISTS (
            SELECT 1 FROM equipment_movements
            WHERE equipment_id = equipment.id
        )"""
    )

    connection.commit()

    print("База данных создана!")
    print("\nКатегории:")
    for row in connection.execute("SELECT * FROM categories"):
        print(row)

    print("\nИнвентарь:")
    for row in connection.execute("SELECT * FROM equipment"):
        print(row)

    print("\nДвижение инвентаря:")
    for row in connection.execute("SELECT * FROM equipment_movements"):
        print(row)

    connection.close()


if __name__ == "__main__":
    create_database()