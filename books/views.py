from django.http import HttpResponse
from django.shortcuts import render

from .models import Book
from reviews.models import Review

def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

def displayBookInfo(request, book_id):
    book = Book.objects.get(pk=book_id)
    reviews = Review.objects.filter(book__id=book_id)
    context = {
        "id": book.id,
        "title": book.title,
        "author": book.author,
        "pub_year": book.pub_year,
        "reviews": reviews
    }
    return render(request, "books/book.html", context);

def ListBooks(request):
    books = Book.objects.all()
    context = {
        "books": books
    }
    return render(request, "books/list.html", context)