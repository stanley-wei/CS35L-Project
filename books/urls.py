from django.urls import path

from . import views
from reviews import views as reviewsViews
from .views import SearchBooks

app_name = "books"
urlpatterns = [
    path("list/", views.ListBooks, name="list_books"),
    path("list/top_ten", views.TopTen, name="top_ten"),

    path("<int:book_id>/", views.displayBookInfo, name="view_book"),
    path("<int:book_id>/review/", reviewsViews.MakeReview, name="review_book"),
    path("<int:book_id>/review/edit", reviewsViews.EditReview, name="edit_review"),

    path("<int:book_id>/review/like_dislike", reviewsViews.LikeDislike, name="like_dislike"),

    path('search/', views.SearchBooks, name='search_books'),

    path('search_isbn/', views.SearchIsbn, name='search_isbn'),
    path('isbn_create/', views.CreateFromIsbn, name='create_from_isbn')
]
