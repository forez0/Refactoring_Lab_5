"""Модуль реалізує патерн Стратегія для пошуку книг за різними критеріями."""


class SearchStrategy:
    """Інтерфейс стратегії пошуку книг."""

    def search(self, books, value):
        """Пошук книг за заданим значенням.

        Аргументи:
            books (list): Список книг для пошуку.
            value (str): Значення для пошуку.

        Повертає:
            list: Список книг, що відповідають критерію пошуку.
        """
        raise NotImplementedError()


class SearchByTitle(SearchStrategy):
    """Стратегія пошуку книг за назвою."""

    def search(self, books, value):
        """Пошук книг за частковим співпадінням у назві (ігнорує регістр)."""
        return [book for book in books if value.lower() in book.title.lower()]


class SearchByAuthor(SearchStrategy):
    """Стратегія пошуку книг за ім'ям автора."""

    def search(self, books, value):
        """Пошук книг за частковим співпадінням в імені автора (ігнорує регістр)."""
        return [book for book in books if value.lower() in book.author.lower()]


class SearchByGenre(SearchStrategy):
    """Стратегія пошуку книг за жанром."""

    def search(self, books, value):
        """Пошук книг за частковим співпадінням у жанрі (ігнорує регістр)."""
        return [book for book in books if value.lower() in book.genre.lower()]
