"""Модуль, що містить модель книги для бібліотечного сервісу."""


class Book:
    """Клас, що представляє книгу з назвою, автором та жанром."""

    def __init__(self, title, author, genre=""):
        self.title = title
        self.author = author
        self.genre = genre

    def __str__(self):
        return f"'{self.title}' автор: {self.author}, жанр: {self.genre}"

    def to_dict(self):
        """Повертає словникове представлення книги."""
        return {
            "title": self.title,
            "author": self.author,
            "genre": self.genre
        }
