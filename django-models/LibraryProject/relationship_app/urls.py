from django.urls import path
from .views import    list_books
from .views import LibraryDetailView
from .views import   register
from .views import LoginView
from .views import LogoutView
from .views import admin_view
from .views import librarian_view
from .views import member_view 

urlpatterns = [
    # Book & Library views
    path('books/', list_books, name='list_books'),
    path('libraries/<int:pk>/', LibraryDetailView.as_view(), name='library_detail'),

    # Authentication views
    path('register/', register, name='register'),
    path('login/', LoginView.as_view(template_name='relationship_app/login.html'), name='login'),
    path('logout/', LogoutView.as_view(template_name='relationship_app/logout.html'), name='logout'),

    # Role-based views
    path('admin-view/', admin_view, name='admin_view'),
    path('librarian-view/', librarian_view, name='librarian_view'),
    path('member-view/', member_view, name='member_view'),
]
