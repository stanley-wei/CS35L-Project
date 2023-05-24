from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from books.models import Book

class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)

    rating = models.IntegerField(blank=False, default=0)
    text = models.CharField(blank=False,max_length=500)
    images = models.ImageField(upload_to='review_images/',blank=True);

    likes= models.ManyToManyField(User, related_name='liked_reviews', blank=True)
    dislikes = models.ManyToManyField(User, related_name='disliked_reviews',blank=True)