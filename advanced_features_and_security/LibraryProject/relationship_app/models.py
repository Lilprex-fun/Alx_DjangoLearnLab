from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver



# Author of books
class Author(models.Model):
	name = models.CharField(max_length=255)

	def __str__(self):
		return self.name


# Book model with ForeignKey to Author
class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    library = models.ForeignKey('Library', on_delete=models.CASCADE)

    class Meta:
        permissions = [
            ("can_add_book", "Can add book"),
            ("can_change_book", "Can change book"),
            ("can_delete_book", "Can delete book"),
        ]

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

class UserProfile(models.Model):
    ROLE_CHOICES = (
        ('Admin', 'Admin'),
        ('Librarian', 'Librarian'),
        ('Member', 'Member'),
    )
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='Member')

    def __str__(self):
        return f"{self.user.username} - {self.role}"

# Signal to automatically create a UserProfile when a new User is created
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

