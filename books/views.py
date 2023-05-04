from django.shortcuts import render

from .models import Book
from reviews.models import Review

def displayBookInfo(request, book_id):
    book = Book.objects.get(pk=book_id)
    reviews = Review.objects.filter(book__id=book_id)
    user_review = None
    if request.user.is_authenticated:
        user_review = reviews.filter(user=request.user)
        reviews = reviews.exclude(user=request.user)
    context = {
        "book": book,
        "reviews": reviews,
        "user_review": None if not user_review else user_review[0],
    }
    return render(request, "books/book.html", context);

def ListBooks(request):
    books = Book.objects.all()
    context = {
        "books": books
    }
    return render(request, "books/list.html", context)

def TopTen(request):
    books = sorted(Book.objects.all(), key=lambda book: book.avg_rating, reverse=True)[:10]
    rankings = {(rank+1): book for rank, book in enumerate(books)}
    context = {
        "rankings": rankings
    }
    return render(request, "books/ranked_list.html", context)