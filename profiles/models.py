from django.db import models

# Create your models here.

from django.contrib.auth.models import User
from django.db import models

from books.models import Book

class UserProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, default=0, related_name="profile")
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    favorite_books = models.ManyToManyField(Book, blank=True)
    followed_users = models.ManyToManyField("self", blank=True, symmetrical=False)

    def __str__(self):
        return str(self.user.id)
    