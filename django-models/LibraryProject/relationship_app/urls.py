from django.urls import path
from .views import list_books      # Function-based view for listing all books
from .views import LibraryDetailView
from .views import (
    register, LoginView, LogoutView,
    admin_view, librarian_view, member_view, 
)  # Class-based view for a specific library
from .views import add_book
from .views import edit_book
from .views import delete_book
urlpatterns = [
    # Function-based view: List all books
    path('books/', list_books, name='list_books'),

    # Class-based view: Show details for a specific library
    path('libraries/<int:pk>/', LibraryDetailView.as_view(), name='library_detail'),

     path('register/', register, name='register'),
    path('login/', LoginView.as_view(template_name='relationship_app/login.html'), name='login'),
    path('logout/', LogoutView.as_view(template_name='relationship_app/logout.html'), name='logout'),

    # ---------- ROLE-BASED VIEWS ----------
    path('admin-view/', admin_view, name='admin_view'),
    path('librarian-view/', librarian_view, name='librarian_view'),
    path('member-view/', member_view, name='member_view'),

    # ---------- SECURED BOOK VIEWS ----------
    path('books/add/', add_book, name='add_book'),
    path('books/<int:pk>/edit/', edit_book, name='edit_book'),
    path('books/<int:pk>/delete/', delete_book, name='delete_book'),
]


