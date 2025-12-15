import os
import sys
import django
from typing import Iterable, Optional


# Ensure project root is on sys.path and Django is configured
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.append(BASE_DIR)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'LibraryProject.settings')
django.setup()

from relationship_app.models import Author, Book, Library, Librarian


def get_books_by_author(author_identifier) -> Iterable[Book]:
    """Return QuerySet of Book for a given author id or name."""
    if isinstance(author_identifier, int):
        return Book.objects.filter(author_id=author_identifier)
    return Book.objects.filter(author__name=author_identifier)


def list_all_books_in_library(library_identifier) -> Iterable[Book]:
    """Return all books in the given library (by id or name).

    If the library does not exist, returns an empty QuerySet.
    """
    if isinstance(library_identifier, int):
        lib = Library.objects.filter(id=library_identifier).first()
    else:
        lib = Library.objects.filter(name=library_identifier).first()
    if not lib:
        return Book.objects.none()
    return lib.books.all()


def get_librarian_for_library(library_identifier) -> Optional[Librarian]:
    """Return the Librarian instance assigned to a library (by id or name).

    Returns None if the library or librarian does not exist.
    """
    if isinstance(library_identifier, int):
        lib = Library.objects.filter(id=library_identifier).select_related('librarian').first()
    else:
        lib = Library.objects.filter(name=library_identifier).select_related('librarian').first()
    if not lib:
        return None
    # Accessing the related object; if missing, attribute access will raise
    try:
        return lib.librarian
    except Librarian.DoesNotExist:
        return None


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Run example relationship queries')
    parser.add_argument('--author', help='Author id or name to list books for')
    parser.add_argument('--library', help='Library id or name to list books for / get librarian')
    args = parser.parse_args()

    if args.author:
        key = int(args.author) if args.author.isdigit() else args.author
        print(f"Books for author={args.author}:")
        for b in get_books_by_author(key):
            print(' -', b.title)

    if args.library:
        key = int(args.library) if args.library.isdigit() else args.library
        print(f"Books in library={args.library}:")
        for b in list_all_books_in_library(key):
            print(' -', b.title)

        lib_librarian = get_librarian_for_library(key)
        print('Librarian:', lib_librarian.name if lib_librarian else 'None')
