from django.urls import path
from .views import list_books      # Function-based view for listing all books
from .views import LibraryDetailView  # Class-based view for a specific library

urlpatterns = [
    # Function-based view: List all books
    path('books/', list_books, name='list_books'),

    # Class-based view: Show details for a specific library
    path('libraries/<int:pk>/', LibraryDetailView.as_view(), name='library_detail'),
]
