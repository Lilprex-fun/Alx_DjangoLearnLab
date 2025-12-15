from django.db import models


# Author of books
class Author(models.Model):
	name = models.CharField(max_length=255)

	def __str__(self):
		return self.name


# Book model with ForeignKey to Author
class Book(models.Model):
	title = models.CharField(max_length=255)
	author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='books')

	def __str__(self):
		return self.title


# Library which holds many books
class Library(models.Model):
	name = models.CharField(max_length=255)
	books = models.ManyToManyField(Book, related_name='libraries', blank=True)

	def __str__(self):
		return self.name


# Librarian assigned one-to-one to a Library
class Librarian(models.Model):
	name = models.CharField(max_length=255)
	library = models.OneToOneField(Library, on_delete=models.CASCADE, related_name='librarian')

	def __str__(self):
		return self.name
