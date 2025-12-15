from django.contrib import admin
from .models import Book


class BookAdmin(admin.ModelAdmin):
	"""
	Custom admin interface for the Book model.
	
	Displays:
	- list_display: Shows title, author, and publication_year in the admin list view
	- list_filter: Filters by author and publication_year for better navigation
	- search_fields: Enables search by title and author name
	- readonly_fields: Displays read-only fields for informational purposes
	"""
	list_display = ("title", "author", "publication_year")
	list_filter = ("author", "publication_year")
	search_fields = ("title", "author__name")
	ordering = ("-publication_year", "title")
	fieldsets = (
		("Book Information", {
			"fields": ("title", "author", "publication_year")
		}),
	)


admin.site.register(Book, BookAdmin)

