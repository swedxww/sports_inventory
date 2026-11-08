from services.category_service import CategoryService
from services.equipment_service import EquipmentService
from services.movement_service import MovementService


def main_menu(user):
    category_service = CategoryService()
    equipment_service = EquipmentService()
    movement_service = MovementService()

    while True:
        print("\n===== ГЛАВНОЕ МЕНЮ =====")
        print("1. Просмотреть категории")
        print("2. Просмотреть инвентарь")
        print("3. Просмотреть историю операций")

        if user.role == "admin":
            print("4. Добавить инвентарь")
            print("5. Удалить инвентарь")

        print("0. Выйти из аккаунта")

        choice = input("Выберите действие: ")

        try:
            if choice == "1":
                categories = category_service.get_all_categories()

                for category in categories:
                    print(category)

            elif choice == "2":
                equipment_list = equipment_service.get_all_equipment()

                for item in equipment_list:
                    print(item)

            elif choice == "3":
                movements = movement_service.get_all_movements()

                for movement in movements:
                    print(movement)

            elif choice == "4" and user.role == "admin":
                name = input("Название инвентаря: ")
                quantity = int(input("Количество: "))
                condition = input("Состояние: ")
                category_id = int(input("ID категории: "))

                equipment_service.add_equipment(
                    user, name, quantity, condition, category_id
                )

                print("Инвентарь добавлен!")

            elif choice == "5" and user.role == "admin":
                equipment_id = int(input("Введите ID инвентаря: "))

                equipment_service.delete_equipment(user, equipment_id)

                print("Инвентарь удалён!")

            elif choice == "0":
                print("Выход из аккаунта...")
                break

            else:
                print("Неверный выбор!")

        except (ValueError, PermissionError) as error:
            print("Ошибка:", error)