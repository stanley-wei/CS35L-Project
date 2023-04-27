from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from books.models import Book

class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)

    rating = models.IntegerField(blank=False, default=0)
    text = models.CharField(max_length=500);