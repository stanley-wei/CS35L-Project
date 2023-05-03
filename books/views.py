from django.http import HttpResponse
from django.shortcuts import render

from .models import Book
from reviews.models import Review

def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

def displayBookInfo(request, book_id):
    book = Book.objects.get(pk=book_id)
    reviews = Review.objects.filter(book__id=book_id)
    user_review = reviews.filter(user=request.user)
    context = {
        "book": book,
        "reviews": reviews.exclude(user=request.user),
        "user_review": None if not user_review else user_review[0],
    }
    return render(request, "books/book.html", context);

def ListBooks(request):
    books = Book.objects.all()
    context = {
        "books": books
    }
    return render(request, "books/list.html", context)