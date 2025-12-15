from django.shortcuts import render, redirect
from django.views.generic import DetailView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Book, Library, UserProfile  # make sure UserProfile is imported


# ---------- BOOK & LIBRARY VIEWS ----------

def list_books(request):
    books = Book.objects.select_related('author').all()
    return render(request, 'relationship_app/list_books.html', {
        'books': books
    })


@login_required
def book_detail(request, pk):
    book = Book.objects.get(pk=pk)
    return render(request, 'relationship_app/book_detail.html', {
        'book': book
    })


class LibraryDetailView(DetailView):
    model = Library
    template_name = 'relationship_app/library_detail.html'
    context_object_name = 'library'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Assuming Book has a ForeignKey to Library named 'library'
        context['books'] = Book.objects.filter(library=self.object)
        return context


# ---------- AUTHENTICATION VIEWS ----------

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Log the user in immediately
            return redirect('list_books')  # Redirect to books page
    else:
        form = UserCreationForm()
    return render(request, 'relationship_app/register.html', {
        'form': form
    })


class LoginView(auth_views.LoginView):
    template_name = 'relationship_app/login.html'


class LogoutView(auth_views.LogoutView):
    template_name = 'relationship_app/logout.html'


# ---------- ROLE-BASED VIEWS ----------

# Helper functions to check roles
def is_admin(user):
    return hasattr(user, 'userprofile') and user.userprofile.role == 'Admin'


def is_librarian(user):
    return hasattr(user, 'userprofile') and user.userprofile.role == 'Librarian'


def is_member(user):
    return hasattr(user, 'userprofile') and user.userprofile.role == 'Member'


# Role-based views
@user_passes_test(lambda u: hasattr(u, 'userprofile') and u.userprofile.role == 'Admin', login_url='login') 
def admin_view(request):
    return render(request, 'relationship_app/admin_view.html')


@user_passes_test(lambda u: hasattr(u, 'userprofile') and u.userprofile.role == 'Librarian', login_url='login')
def librarian_view(request):
    return render(request, 'relationship_app/librarian_view.html')


@user_passes_test(lambda u: hasattr(u, 'userprofile') and u.userprofile.role == 'Member', login_url='login')
def member_view(request):
    return render(request, 'relationship_app/member_view.html')


 