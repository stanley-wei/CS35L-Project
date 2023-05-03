from django.urls import path

from . import views
from reviews import views as reviewsViews

app_name = "books"
urlpatterns = [
    path("list/", views.ListBooks, name="list_books"),
    path("<int:book_id>/", views.displayBookInfo, name="view_book"),
    path("<int:book_id>/review/", reviewsViews.MakeReview, name="review_book"),
    path("<int:book_id>/review/edit", reviewsViews.EditReview, name="edit_review")
]
