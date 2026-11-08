from repositories.movement_repository import MovementRepository
from repositories.equipment_repository import EquipmentRepository


class MovementService:

    def __init__(self):
        self.repository = MovementRepository()
        self.equipment_repository = EquipmentRepository()

    # Проверка прав администратора
    def check_admin(self, user):
        if user is None or user.role != "admin":
            raise PermissionError("Недостаточно прав для выполнения операции")

    # Добавление операции
    def add_movement(self, user, equipment_id, movement_type, quantity, movement_date):
        self.check_admin(user)

        equipment = self.equipment_repository.get_by_id(equipment_id)

        if equipment is None:
            raise ValueError("Инвентарь не найден")

        if movement_type not in ["Поступление", "Списание"]:
            raise ValueError("Неверный тип операции")

        if quantity <= 0:
            raise ValueError("Количество должно быть больше нуля")

        if not movement_date.strip():
            raise ValueError("Необходимо указать дату")

        # Рассчитываем новое количество
        if movement_type == "Поступление":
            new_quantity = equipment.quantity + quantity
        else:
            new_quantity = equipment.quantity - quantity

        if new_quantity < 0:
            raise ValueError("Нельзя списать больше инвентаря, чем есть в наличии")

        # Обновляем количество инвентаря
        self.equipment_repository.update(
            equipment.id,
            equipment.name,
            new_quantity,
            equipment.condition,
            equipment.category_id
        )

        # Записываем операцию в историю
        self.repository.add(
            equipment_id,
            movement_type,
            quantity,
            movement_date.strip()
        )

    # Получение истории операций
    def get_all_movements(self):
        return self.repository.get_all()