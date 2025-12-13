"""
Simple query examples for relationship_app models.

Provides:
- get_books_by_author(author_name)
- get_books_in_library(library_name)
- get_librarian_for_library(library_name)

Run as a small CLI demo:
    python manage.py shell < relationship_app/query_samples.py
or
    python relationship_app/query_samples.py "Author Name" "Library Name"

Note: This script configures Django settings so it can be run directly from the project root.
"""

import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "LibraryProject.settings")
django.setup()

from relationship_app.models import Author, Book, Library, Librarian
from django.db.models import QuerySet
from typing import Optional


def get_books_by_author(author_name: str) -> QuerySet:
    """Return a queryset of Book objects written by `author_name`.

    Matches on `Author.name` (case-sensitive exact match). For partial or case-insensitive
    searches, use `author__name__icontains` instead of `author__name`.
    """
    return Book.objects.filter(author__name=author_name)


def get_books_in_library(library_name: str) -> QuerySet:
    """Return a queryset of Book objects that belong to the library named `library_name`.

    If the library does not exist, an empty queryset is returned.
    """
    try:
        library = Library.objects.get(name=library_name)
    except Library.DoesNotExist:
        return Book.objects.none()
    return library.books.all()


def get_librarian_for_library(library_name: str) -> Optional[Librarian]:
    """Return the Librarian instance assigned to the library named `library_name`.

    Returns `None` if the library or its librarian does not exist.
    """
    try:
        library = Library.objects.get(name=library_name)
    except Library.DoesNotExist:
        return None

    # Use the related name on OneToOneField (set as `librarian` in the model)
    return getattr(library, "librarian", None)


if __name__ == "__main__":
    import sys

    author_arg = sys.argv[1] if len(sys.argv) > 1 else None
    library_arg = sys.argv[2] if len(sys.argv) > 2 else None

    if author_arg:
        print(f"Books by '{author_arg}':")
        for book in get_books_by_author(author_arg):
            year = book.publication_year if hasattr(book, "publication_year") else "?"
            print(f"- {book.title} ({year})")

    if library_arg:
        print(f"\nBooks in library '{library_arg}':")
        for book in get_books_in_library(library_arg):
            print(f"- {book.title} — {book.author.name}")

        librarian = get_librarian_for_library(library_arg)
        print(f"\nLibrarian for '{library_arg}': {librarian.name if librarian else 'None'}")
