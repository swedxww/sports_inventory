import hashlib
from repositories.user_repository import UserRepository


class AuthService:

    def __init__(self):
        self.repository = UserRepository()

    # Создание хеша пароля
    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    # Регистрация пользователя
    def register(self, login, password):
        if not login.strip():
            raise ValueError("Введите логин")

        if len(password) < 4:
            raise ValueError("Пароль должен содержать минимум 4 символа")

        if self.repository.get_by_login(login.strip()) is not None:
            raise ValueError("Такой пользователь уже существует")

        password_hash = self.hash_password(password)

        self.repository.add(login.strip(), password_hash, "user")

    # Авторизация пользователя
    def login(self, login, password):
        user = self.repository.get_by_login(login.strip())

        if user is None:
            raise ValueError("Пользователь не найден")

        password_hash = self.hash_password(password)

        if user.password_hash != password_hash:
            raise ValueError("Неверный пароль")

        return user