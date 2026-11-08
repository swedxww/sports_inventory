from database import create_database
from ui.auth import start_auth
from ui.menu import main_menu


def main():
    create_database()

    while True:
        user = start_auth()

        if user is None:
            print("Программа завершена.")
            break

        main_menu(user)


if __name__ == "__main__":
    main()