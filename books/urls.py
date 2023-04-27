from django.urls import path

from . import views
from reviews import views as reviewsViews

urlpatterns = [
    path("", views.index, name="index"),
    path("list/", views.ListBooks, name="list_books"),
    path("<int:book_id>/", views.displayBookInfo, name="book"),
    path("<int:book_id>/review/", reviewsViews.MakeReview, name="review_book")
]