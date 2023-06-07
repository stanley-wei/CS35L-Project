from django.db import models
from utilities import decimalize

class Book(models.Model):
    title = models.CharField(max_length=200, blank=False)
    author = models.CharField(max_length=200)
    pub_year = models.IntegerField(default=-1, blank=True)
    isbn = models.CharField(max_length=13, blank=True)

    olid = models.CharField(max_length=11, blank=True)
    num_pages = models.IntegerField(blank=True, null=True)

    @property
    def avg_rating(self):
        return decimalize(self.review_set.aggregate(
                avg=models.Avg('rating'))['avg'])
