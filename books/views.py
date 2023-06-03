from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from .models import Book
from reviews.models import Review
from .forms import BookSearchForm, IsbnSearchForm

from django.db.models import Q
from profiles.models import UserProfile

from datetime import datetime
import re
from olclient.openlibrary import OpenLibrary

def Home(request):
    return render(request, 'books/home.html')

def displayBookInfo(request, book_id):
    book = Book.objects.get(pk=book_id)
    reviews = Review.objects.filter(book__id=book_id)
    user_review = None
    profile = None
    if request.user.is_authenticated:
        user_review = reviews.filter(user=request.user)
        reviews = reviews.exclude(user=request.user)
        try:
            profile = UserProfile.objects.filter(user=request.user)[0] 
        except:
            profile = UserProfile.objects.create(user=request.user)

    sort_options = request.GET.get('sort')
    if sort_options == 'favorable':
        reviews = reviews.order_by('-rating')  # Sort by most favorable
    elif sort_options == 'unfavorable':
        reviews = reviews.order_by('rating')  # Sort by least favorable

    context = {
        "book": book,
        "reviews": reviews,
        "user_review": None if not user_review else user_review[0],
        "profile": profile
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
    
def SearchBooks(request):
    form = BookSearchForm(request.GET)
    results = []
    query = None;

    if form.is_valid():
        query = form.cleaned_data['query']
        results = Book.objects.filter(Q(title__icontains=query)|Q(author__icontains=query))

        sort_options = request.GET.get('sort-search')
        if sort_options == 'alphabetical':
            results = results.order_by('title')
        elif sort_options == 'highest-rated':
            results = sorted(results, key=lambda book: book.avg_rating, reverse=True)
        elif sort_options == 'lowest-rated':
            results = sorted(results, key=lambda book: book.avg_rating)

    return render(request, 'books/search_results.html', {'form': form, 'results': results, 'query':query})

@login_required
def FavoriteBook(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    user = request.user

    try:
        profile = UserProfile.objects.filter(user=user)[0] 
    except:
        profile = UserProfile.objects.create(user=user)

    if book in profile.favorite_books.all():
        profile.favorite_books.remove(book)
    else:
        profile.favorite_books.add(book)

    profile.save()
    return redirect("books:view_book", book_id=book_id)

def SearchIsbn(request):
    form = IsbnSearchForm(request.GET)
    query = None;

    title = None;
    authors = None;
    pub_year = None;

    if form.is_valid():
        query = form.cleaned_data['isbn']
        ol = OpenLibrary()

        edition = ol.Edition.get(isbn=query)
        if(edition):
            title = edition.title;
            authors = ', '.join(author_obj.name for author_obj in edition.authors)
            t = re.search('\d{% s}'% 4, edition.publish_date)
            pub_year = (int(t.group(0)) if t else None)

    context = {
        'form': form,
        'query': query,

        'title': title,
        'authors': authors,
        'pub_year': pub_year,
    }

    return render(request, 'books/isbn.html', context)

def CreateFromIsbn(request):
    isbn = request.GET.get('isbn', "")
    ol = OpenLibrary()
    edition = ol.Edition.get(isbn=isbn)

    t = re.search('\d{% s}'% 4, edition.publish_date)
    pub_year = (int(t.group(0)) if t else None)

    book_obj = Book(title = edition.title, 
                     author = ', '.join(author_obj.name for author_obj in edition.authors),
                     isbn=isbn,
                     pub_year = pub_year)
    book_obj.save()

    return displayBookInfo(request, book_obj.id)
