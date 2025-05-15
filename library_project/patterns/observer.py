"""Модуль, що реалізує патерн спостерігача (Observer) для системи сповіщень."""

class Notifier:
    """Клас, який управляє списком спостерігачів і надсилає їм сповіщення."""

    def __init__(self):
        """Ініціалізує порожній список спостерігачів."""
        self.observers = []

    def add_observer(self, observer):
        """Додає нового спостерігача, якщо його ще немає в списку.

        Args:
            observer: Об'єкт, який має метод notify(message)
        """
        if observer not in self.observers:
            self.observers.append(observer)

    def remove_observer(self, observer):
        """Видаляє спостерігача зі списку, якщо він там є.

        Args:
            observer: Об'єкт-спостерігач для видалення
        """
        if observer in self.observers:
            self.observers.remove(observer)

    def notify_all(self, message):
        """Надсилає сповіщення всім зареєстрованим спостерігачам.

        Args:
            message (str): Повідомлення для розсилки спостерігачам
        """
        for observer in self.observers:
            observer.notify(message)
