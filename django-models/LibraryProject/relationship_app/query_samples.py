from relationship_app.models import Author, Book, Library, Librarian
from typing import Iterable, Optional


def get_books_by_author(author_identifier) -> Iterable[Book]:
    try:
     
        if isinstance(author_identifier, int):
              author = Author.objects.get(id=author_identifier)
        else:
              author_name = author_identifier
              author = Author.objects.get(name=author_name)   
        return Book.objects.filter(author=author)
    except Author.DoesNotExist:
        return Book.objects.none()


def list_all_books_in_library(library_identifier) -> Iterable[Book]:
    try:
        if isinstance(library_identifier, int):
            library = Library.objects.get(id=library_identifier)
        else:
            library_name = library_identifier
            library = Library.objects.get(name=library_name)
        return library.books.all()
    except Library.DoesNotExist:
        return Book.objects.none()


def get_librarian_for_library(library_identifier) -> Optional[Librarian]:
    try:
        if isinstance(library_identifier, int):
            library = Library.objects.get(id=library_identifier)
        else:
            library_name = library_identifier
            library = Library.objects.get(name=library_name)
        return Librarian.objects.get(library=library)   
    except (Library.DoesNotExist, Librarian.DoesNotExist):
        return None
