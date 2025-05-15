"""Модуль, що містить моделі користувачів для бібліотечного сервісу."""


class User:
    """Базовий клас користувача з іменем та методом сповіщення."""

    def __init__(self, name):
        """Ініціалізує користувача з ім’ям."""
        self.name = name

    def notify(self, message):
        """Виводить сповіщення для користувача."""
        print(f"{self.name} отримав сповіщення: {message}")

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"{self.__class__.__name__}('{self.name}')"


class Reader(User):
    """Клас читача, успадковує поведінку базового користувача."""
    def favorite_genre(self):
        """Метод-заглушка для демонстрації публічного API."""
        return "Невідомо"


class Librarian(User):
    """Клас бібліотекаря, успадковує поведінку базового користувача."""
    def permission_level(self):
        """Метод-заглушка для демонстрації публічного API."""
        return "Адміністратор"


class UserFactory:
    """Фабрика для створення користувачів відповідно до ролі."""

    @staticmethod
    def create_user(role, name):
        """Створює екземпляр користувача заданої ролі.

        Аргументи:
            role (str): Роль користувача (reader або librarian)
            name (str): Ім’я користувача

        Повертає:
            User: Екземпляр Reader або Librarian

        Породжує:
            ValueError: Якщо роль невідома
        """
        if role == "reader":
            return Reader(name)
        if role == "librarian":
            return Librarian(name)
        raise ValueError("Невідома роль користувача")
