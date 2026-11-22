import csv
import json
from pathlib import Path
import xml.etree.ElementTree as ET

import yaml

from database import get_connection


SQL = """
SELECT e.id, e.name, e.quantity, e.condition,
       c.id          AS category_id,
       c.name        AS category_name,
       c.description AS category_description
FROM equipment e
JOIN categories c ON e.category_id = c.id
"""

PREFIX = "category_"
NESTED_NAME = "category"
ROOT_NAME = "equipment_list"
ITEM_NAME = "equipment"

OUT_DIR = Path(__file__).parent / "out"


def get_rows():
    connection = get_connection()
    cursor = connection.execute(SQL)

    columns = [item[0] for item in cursor.description]
    rows = [dict(zip(columns, row)) for row in cursor.fetchall()]

    connection.close()
    return columns, rows


def make_nested(rows):
    result = []
    for row in rows:
        item = {}
        nested = {}
        for key, value in row.items():
            if key.startswith(PREFIX):
                nested[key[len(PREFIX):]] = value
            else:
                item[key] = value
        item[NESTED_NAME] = nested
        result.append(item)
    return result

def save_json(data):
    with open(OUT_DIR / "data.json", "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

def save_csv(columns, rows):
    with open(OUT_DIR / "data.csv", "w", encoding="utf-8-sig", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=columns)
        writer.writeheader()
        writer.writerows(rows)


def save_xml(data):
    root = ET.Element(ROOT_NAME)

    for item in data:
        item_tag = ET.SubElement(root, ITEM_NAME)
        for key, value in item.items():
            if isinstance(value, dict):
                nested_tag = ET.SubElement(item_tag, key)
                for nested_key, nested_value in value.items():
                    ET.SubElement(nested_tag, nested_key).text = str(nested_value)
            else:
                ET.SubElement(item_tag, key).text = str(value)

    ET.indent(root)
    ET.ElementTree(root).write(OUT_DIR / "data.xml", encoding="utf-8", xml_declaration=True)


def save_yaml(data):
    with open(OUT_DIR / "data.yaml", "w", encoding="utf-8") as file:
        yaml.dump(data, file, allow_unicode=True, sort_keys=False)


def main():
    OUT_DIR.mkdir(exist_ok=True)

    columns, rows = get_rows()
    nested_data = make_nested(rows)

    save_json(nested_data)
    save_csv(columns, rows)
    save_xml(nested_data)
    save_yaml(nested_data)

    print("Готово! Записей:", len(rows))


if __name__ == "__main__":
    main()