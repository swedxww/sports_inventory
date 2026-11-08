from services.auth_service import AuthService


def start_auth():
    service = AuthService()

    while True:
        print("\n===== SPORTS INVENTORY =====")
        print("1. Войти")
        print("2. Зарегистрироваться")
        print("3. Выход")

        choice = input("Выберите действие: ")

        if choice == "1":
            login = input("Логин: ")
            password = input("Пароль: ")

            try:
                user = service.login(login, password)
                print(f"\nДобро пожаловать, {user.login}!")
                return user

            except ValueError as error:
                print("Ошибка:", error)

        elif choice == "2":
            login = input("Придумайте логин: ")
            password = input("Придумайте пароль: ")

            try:
                service.register(login, password)
                print("Регистрация прошла успешно!")

            except ValueError as error:
                print("Ошибка:", error)

        elif choice == "3":
            return None

        else:
            print("Неверный выбор!")