from django.shortcuts import render, redirect
from django.views.generic import DetailView
from django.contrib.auth import login  # <-- Add this
from django.contrib.auth.forms import UserCreationForm  # <-- Make sure this is present
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from .models import Book, Library


# ---------- BOOK & LIBRARY VIEWS ----------

def list_books(request):
    books = Book.objects.select_related('author').all()
    return render(request, 'relationship_app/list_books.html', {
        'books': books
    })


class LibraryDetailView(DetailView):
    model = Library
    template_name = 'relationship_app/library_detail.html'
    context_object_name = 'library'


# ---------- AUTHENTICATION VIEWS ----------

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()

    return render(request, 'relationship_app/register.html', {
        'form': form
    })
class LoginView(auth_views.LoginView):
    template_name = 'relationship_app/login.html'

class LogoutView(auth_views.LogoutView):
    template_name = 'relationship_app/logout.html'
 