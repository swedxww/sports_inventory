import sqlite3
from pathlib import Path


DB_PATH = Path(__file__).parent / "database" / "sports_inventory.db"
SCHEMA_PATH = Path(__file__).parent / "database" / "schema.sql"


# Подключение к базе данных
def get_connection():
    connection = sqlite3.connect(DB_PATH)
    connection.execute("PRAGMA foreign_keys = ON")
    return connection


# Создание базы данных
def create_database():
    connection = get_connection()

    # Читаем файл со структурой таблиц
    with open(SCHEMA_PATH, "r", encoding="utf-8") as file:
        schema = file.read()

    connection.executescript(schema)

    # Добавляем категории
    connection.execute(
        "INSERT OR IGNORE INTO categories (name, description) VALUES (?, ?)",
        ("Мячи", "Спортивные мячи")
    )

    connection.execute(
        "INSERT OR IGNORE INTO categories (name, description) VALUES (?, ?)",
        ("Гантели", "Силовой инвентарь")
    )

    # Находим ID категорий
    ball_category = connection.execute(
        "SELECT id FROM categories WHERE name = 'Мячи'"
    ).fetchone()[0]

    dumbbell_category = connection.execute(
        "SELECT id FROM categories WHERE name = 'Гантели'"
    ).fetchone()[0]

    # Проверяем наличие футбольного мяча
    ball = connection.execute(
        "SELECT id FROM equipment WHERE name = ?",
        ("Футбольный мяч",)
    ).fetchone()

    if ball is None:
        connection.execute(
            """INSERT INTO equipment
            (name, quantity, condition, category_id)
            VALUES (?, ?, ?, ?)""",
            ("Футбольный мяч", 10, "Хорошее", ball_category)
        )

    # Проверяем наличие гантелей
    dumbbells = connection.execute(
        "SELECT id FROM equipment WHERE name = ?",
        ("Гантели 5 кг",)
    ).fetchone()

    if dumbbells is None:
        connection.execute(
            """INSERT INTO equipment
            (name, quantity, condition, category_id)
            VALUES (?, ?, ?, ?)""",
            ("Гантели 5 кг", 8, "Хорошее", dumbbell_category)
        )

    # Добавляем начальную операцию поступления
    ball_id = connection.execute(
        "SELECT id FROM equipment WHERE name = 'Футбольный мяч'"
    ).fetchone()[0]

    movement = connection.execute(
        "SELECT id FROM equipment_movements WHERE equipment_id = ?",
        (ball_id,)
    ).fetchone()

    if movement is None:
        connection.execute(
            """
            INSERT INTO equipment_movements
            (equipment_id, movement_type, quantity, movement_date)
            VALUES (?, ?, ?, ?)
            """,
            (ball_id, "Поступление", 10, "2026-10-26")
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