"""
Модуль сервісу бібліотеки.
Містить клас LibraryService для роботи з книгами, користувачами та видачею книг.
Визначені власні виключення для обробки помилок.
"""

from library_project.patterns import SingletonMeta, Notifier
from library_project.models import Book


class LibraryError(Exception):
    """Базове виключення для бібліотеки."""


class BookExistsError(LibraryError):
    """Виключення при додаванні книги, яка вже існує."""


class UserExistsError(LibraryError):
    """Виключення при додаванні користувача, який вже існує."""


class BookNotFoundError(LibraryError):
    """Виключення, коли книга не знайдена у бібліотеці."""


class BookUnavailableError(LibraryError):
    """Виключення, коли книга вже зайнята іншим користувачем."""


class ReturnBookError(LibraryError):
    """Виключення при спробі повернути книгу, яку не можна повернути."""


class LibraryService(metaclass=SingletonMeta):
    """Сервіс для роботи з бібліотекою (додавання книг, користувачів, видача книг)."""

    def __init__(self):
        self.books = []
        self.users = []
        self.lent_books = {}  # {Book: User}
        self.notifier = Notifier()

    def add_book(self, book: Book):
        """Додає книгу до бібліотеки, якщо вона ще не існує."""
        if any(b.title == book.title and b.author == book.author for b in self.books):
            raise BookExistsError("Книга з таким самим автором і назвою вже існує")
        self.books.append(book)
        self.notifier.notify_all(f"Додано книгу '{book.title}' автора {book.author}")

    def register_user(self, user):
        """Реєструє нового користувача, якщо такого ще немає."""
        if any(u.name == user.name and u.__class__ == user.__class__ for u in self.users):
            raise UserExistsError("Користувач з таким ім'ям і типом вже існує")
        self.users.append(user)
        self.notifier.notify_all(f"Зареєстровано користувача '{user.name}'")

    def get_users(self):
        """Повертає список усіх зареєстрованих користувачів."""
        return self.users

    def get_books_by_user(self, user):
        """Повертає список книг, які користувач наразі взяв."""
        return [book for book, u in self.lent_books.items() if u == user]

    def lend_book(self, book, user):
        """Видає книгу користувачу, якщо книга доступна в бібліотеці."""
        if book not in self.books:
            raise BookNotFoundError("Такої книги немає в бібліотеці")
        if book in self.lent_books:
            raise BookUnavailableError("Книга вже зайнята")
        self.lent_books[book] = user
        self.notifier.notify_all(f"Книга '{book.title}' видана користувачу {user.name}")

    def return_book(self, book, user):
        """Приймає книгу назад від користувача."""
        if self.lent_books.get(book) != user:
            raise ReturnBookError("Цю книгу не може повернути цей користувач")
        del self.lent_books[book]
        self.notifier.notify_all(f"Книга '{book.title}' повернена користувачем {user.name}")

    def add_observer(self, observer):
        """Додає спостерігача (наблюдателя) для повідомлень."""
        self.notifier.add_observer(observer)

    def remove_observer(self, observer):
        """Видаляє спостерігача (наблюдателя) з повідомлень."""
        self.notifier.remove_observer(observer)
