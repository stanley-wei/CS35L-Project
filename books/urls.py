from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("list/", views.ListBooks, name="list_books"),
    path("<int:book_id>/", views.displayBookInfo, name="book"),
]