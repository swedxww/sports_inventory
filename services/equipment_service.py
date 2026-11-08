from repositories.equipment_repository import EquipmentRepository
from repositories.category_repository import CategoryRepository


class EquipmentService:

    def __init__(self):
        self.repository = EquipmentRepository()
        self.category_repository = CategoryRepository()

    # Проверка прав администратора
    def check_admin(self, user):
        if user is None or user.role != "admin":
            raise PermissionError("Недостаточно прав для выполнения операции")

    # Добавление инвентаря
    def add_equipment(self, user, name, quantity, condition, category_id):
        self.check_admin(user)

        if not name.strip():
            raise ValueError("Название инвентаря не может быть пустым")

        if quantity < 0:
            raise ValueError("Количество не может быть отрицательным")

        category = self.category_repository.get_by_id(category_id)

        if category is None:
            raise ValueError("Указанная категория не существует")

        self.repository.add(name.strip(), quantity, condition, category_id)

    # Получение всего инвентаря
    def get_all_equipment(self):
        return self.repository.get_all()

    # Поиск инвентаря по ID
    def get_equipment(self, equipment_id):
        equipment = self.repository.get_by_id(equipment_id)

        if equipment is None:
            raise ValueError("Инвентарь не найден")

        return equipment

    # Изменение инвентаря
    def update_equipment(self, user, equipment_id, name, quantity, condition, category_id):
        self.check_admin(user)
        self.get_equipment(equipment_id)

        if not name.strip():
            raise ValueError("Название инвентаря не может быть пустым")

        if quantity < 0:
            raise ValueError("Количество не может быть отрицательным")

        category = self.category_repository.get_by_id(category_id)

        if category is None:
            raise ValueError("Указанная категория не существует")

        self.repository.update(
            equipment_id, name.strip(), quantity, condition, category_id
        )

    # Удаление инвентаря
    def delete_equipment(self, user, equipment_id):
        self.check_admin(user)
        self.get_equipment(equipment_id)
        self.repository.delete(equipment_id)