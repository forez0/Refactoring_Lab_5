from library_project.services.library import LibraryService
from library_project.models.user import UserFactory  # ← виправлено
from library_project.models.book import Book         # ← виправлено
from library_project.patterns import SearchByTitle, SearchByAuthor, SearchByGenre
from unittest.mock import MagicMock

def test_singleton():
    a = LibraryService()
    b = LibraryService()
    assert a is b

def test_add_book():
    library = LibraryService()
    book = Book("Python 101", "John Doe", "Programming")
    library.add_book(book)
    assert book in library.books

def test_factory_reader():
    user = UserFactory.create_user("reader", "Anna")
    assert user.__class__.__name__ == "Reader"

def test_factory_librarian():
    user = UserFactory.create_user("librarian", "Oleh")
    assert user.__class__.__name__ == "Librarian"

def test_strategy_title():
    books = [Book("Book1", "A", "Drama"), Book("Book2", "B", "Sci-Fi")]
    strategy = SearchByTitle()
    result = strategy.search(books, "Book1")
    assert len(result) == 1 and result[0].title == "Book1"

def test_strategy_author():
    books = [Book("X", "Author1", "Drama"), Book("Y", "Author2", "Sci-Fi")]
    strategy = SearchByAuthor()
    result = strategy.search(books, "Author2")
    assert len(result) == 1 and result[0].author == "Author2"

def test_strategy_genre():
    books = [Book("X", "A", "Fantasy"), Book("Y", "B", "Sci-Fi")]
    strategy = SearchByGenre()
    result = strategy.search(books, "Sci-Fi")
    assert len(result) == 1 and result[0].genre == "Sci-Fi"


def test_observer_notify(capsys):
    library = LibraryService()
    reader = UserFactory.create_user("reader", "Ivan")
    library.add_observer(reader)  # через метод сервісу
    book = Book("Design Patterns", "GoF", "Software")
    library.add_book(book)

    captured = capsys.readouterr()
    assert "отримав сповіщення" in captured.out


def test_remove_observer():
    library = LibraryService()
    reader = UserFactory.create_user("reader", "Marta")

    # Замінюємо метод notify мок-об'єктом
    reader.notify = MagicMock()

    library.add_observer(reader)
    library.remove_observer(reader)

    book = Book("Python Advanced", "Expert", "Tech")
    library.add_book(book)

    # Після видалення notify викликатись не повинен
    reader.notify.assert_not_called()


def test_search_multiple_books():
    library = LibraryService()
    library.books = [
        Book("Clean Code", "Robert Martin", "Software"),
        Book("Clean Architecture", "Robert Martin", "Software"),
        Book("Python Tricks", "Dan Bader", "Programming"),
    ]
    strategy = SearchByAuthor()
    result = strategy.search(library.books, "Robert Martin")
    assert len(result) == 2
