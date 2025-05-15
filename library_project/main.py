"""Головний вхідний пункт системи управління бібліотекою.

Цей модуль надає інтерфейс командного рядка для системи бібліотеки,
обробляючи взаємодію з користувачем, управління книгами та системні операції.
"""

from library_project.services.library import LibraryService
from library_project.models import Book
from library_project.models.user import UserFactory, Librarian
from library_project.patterns.strategy import (
    SearchByTitle,
    SearchByAuthor,
    SearchByGenre
)


class NotificationPrinter:
    """Обробляє відображення системних сповіщень для користувача."""

    def notify(self, message):
        """Відображає повідомлення-сповіщення.

        Аргументи:
            message (str): Повідомлення для відображення
        """
        print(f"[Повідомлення]: {message}")


def choose_from_list(items, item_name):
    """Запитує у користувача вибір елементу зі списку.

    Аргументи:
        items: Список елементів для вибору
        item_name: Описова назва типу елементу для відображення

    Повертає:
        Обраний елемент або None, якщо скасовано
    """
    if not items:
        print(f"Немає доступних {item_name}.")
        return None
    print(f"Оберіть {item_name}:")
    for idx, item in enumerate(items, 1):
        print(f"{idx}. {item}")
    while True:
        choice = input(f"Введіть номер {item_name} (або 'q' для відміни): ")
        if choice.lower() == 'q':
            return None
        if choice.isdigit() and 1 <= int(choice) <= len(items):
            return items[int(choice) - 1]
        print("Невірний вибір, спробуйте ще.")


def display_book_status(book, service):
    """Генерує форматований рядок стану книги.

    Аргументи:
        book: Об'єкт книги
        service: Екземпляр LibraryService

    Повертає:
        Форматований рядок стану
    """
    if book not in service.lent_books:
        return f"- {book} (вільна)"
    return f"- {book} (видана користувачу {service.lent_books[book].name})"


def search_books(service):
    """Обробляє функціонал пошуку книг.

    Аргументи:
        service: Екземпляр LibraryService
    """
    print("\n--- Пошук книги ---")
    print("Оберіть тип пошуку:")
    print("1. За назвою")
    print("2. За автором")
    print("3. За жанром")
    choice = input("Введіть номер: ")

    if choice not in ('1', '2', '3'):
        print("Невірний вибір")
        return

    query = input("Введіть пошуковий запит: ")
    strategies = {
        '1': SearchByTitle(),
        '2': SearchByAuthor(),
        '3': SearchByGenre()
    }

    results = strategies[choice].search(service.books, query)
    if not results:
        print("Книги не знайдено.")
    else:
        print("Знайдені книги:")
        for book in results:
            print(display_book_status(book, service))


def register_user(service):
    """Обробляє реєстрацію нового користувача.

    Аргументи:
        service: Екземпляр LibraryService

    Повертає:
        Створений об'єкт User або None у разі невдачі
    """
    print("\n--- Реєстрація користувача ---")
    name = input("Введіть ім'я користувача: ")
    role = input("Оберіть роль (reader/librarian): ").strip().lower()

    if role not in ('reader', 'librarian'):
        print("Невідома роль. Спробуйте ще.")
        return None

    try:
        user = UserFactory.create_user(role, name)
        service.register_user(user)
        print(f"Користувача {name} з роллю {role} зареєстровано.")
        return user
    except ValueError as e:
        print("Помилка:", e)
        return None


def login(service):
    """Обробляє процес входу користувача.

    Аргументи:
        service: Екземпляр LibraryService

    Повертає:
        Об'єкт User, що увійшов у систему, або None, якщо скасовано
    """
    if not service.users:
        print("Поки що немає зареєстрованих користувачів. Зареєструйтесь.")
        return None

    print("\n--- Вхід у систему ---")
    user = choose_from_list(service.users, "користувача")
    if user:
        print(f"Ви увійшли як {user.name} ({user.__class__.__name__})")
    return user


def handle_librarian_menu(service, librarian):
    """Обробляє опції меню для бібліотекарів.

    Аргументи:
        service: Екземпляр LibraryService
        librarian: Об'єкт Librarian, що увійшов у систему

    Повертає:
        Об'єкт Librarian або None при виході
    """
    print(f"\n--- Меню бібліотеки ({librarian.name}, Бібліотекар) ---")
    print("1. Додати книгу")
    print("2. Показати всі книги")
    print("3. Показати всіх користувачів")
    print("0. Вийти з аккаунту")

    choice = input("Виберіть опцію: ")

    if choice == '1':
        title = input("Введіть назву книги: ")
        author = input("Введіть автора книги: ")
        genre = input("Введіть жанр книги: ")
        try:
            service.add_book(Book(title, author, genre))
            print("Книгу додано.")
        except ValueError as e:
            print("Помилка:", e)

    elif choice == '2':
        if not service.books:
            print("Книги відсутні.")
        else:
            print("Книги в бібліотеці:")
            for book in service.books:
                print(display_book_status(book, service))

    elif choice == '3':
        if not service.users:
            print("Користувачі відсутні.")
        else:
            print("Зареєстровані користувачі:")
            for user in service.users:
                print(f"- {user}")

    elif choice == '0':
        print(f"Вихід з аккаунту {librarian.name}")
        return None

    return librarian


def handle_reader_menu(service, reader):
    """Обробляє опції меню для читачів.

    Аргументи:
        service: Екземпляр LibraryService
        reader: Об'єкт Reader, що увійшов у систему

    Повертає:
        Об'єкт Reader або None при виході
    """
    print(f"\n--- Меню бібліотеки ({reader.name}, Читач) ---")
    print("1. Вибрати книгу")
    print("2. Повернути книгу")
    print("3. Показати всі книги")
    print("4. Показати книги користувача")
    print("5. Пошук книги")
    print("0. Вийти з аккаунту")

    choice = input("Виберіть опцію: ")

    if choice == '1':
        book = choose_from_list(service.books, "книгу")
        if book:
            try:
                service.lend_book(book, reader)
            except ValueError as e:
                print("Помилка:", e)

    elif choice == '2':
        user_books = service.get_books_by_user(reader)
        if not user_books:
            print("Ви не маєте виданих книг.")
        else:
            book = choose_from_list(user_books, "книгу для повернення")
            if book:
                try:
                    service.return_book(book, reader)
                except ValueError as e:
                    print("Помилка:", e)

    elif choice == '3':
        if not service.books:
            print("Книги відсутні.")
        else:
            print("Книги в бібліотеці:")
            for book in service.books:
                print(display_book_status(book, service))

    elif choice == '4':
        books = service.get_books_by_user(reader)
        if not books:
            print("Ви не маєте виданих книг.")
        else:
            print("Ваші книги:")
            for book in books:
                print(f"- {book}")

    elif choice == '5':
        search_books(service)

    elif choice == '0':
        print(f"Вихід з аккаунту {reader.name}")
        return None

    return reader


def handle_unauthenticated_menu(service):
    """Обробляє опції меню для неавторизованих користувачів.

    Аргументи:
        service: Екземпляр LibraryService

    Повертає:
        Об'єкт User при успішному вході/реєстрації, інакше None
    """
    print("\n--- Головне меню ---")
    print("1. Зареєструватися")
    print("2. Увійти")
    print("0. Вийти")

    choice = input("Виберіть опцію: ")

    if choice == '1':
        return register_user(service)
    elif choice == '2':
        user = login(service)
        return user
    elif choice == '0':
        print("Вихід...")
        exit()
    else:
        print("Невідома команда, спробуйте ще.")
    return None


def main():
    """Головна точка входу додатку."""
    service = LibraryService()
    service.add_observer(NotificationPrinter())
    current_user = None

    while True:
        if current_user is None:
            current_user = handle_unauthenticated_menu(service)
        else:
            if isinstance(current_user, Librarian):
                current_user = handle_librarian_menu(service, current_user)
            else:
                current_user = handle_reader_menu(service, current_user)


if __name__ == "__main__":
    main()
