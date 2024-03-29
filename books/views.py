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
    elif sort_options == 'helpful':
        reviews = reviews.order_by('-likes')  # Sort by least favorable
    elif sort_options == 'unhelpful':
        reviews = reviews.order_by('-dislikes')  # Sort by least favorable    

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
    field = None;

    if form.is_valid():
        query = form.cleaned_data['query']
        field = request.GET.get('field', 'title')
        min_score = request.GET.get('min')
        max_score = request.GET.get('max')
        min_year = request.GET.get('after')
        max_year = request.GET.get('before')

        if field == 'author':
            results = Book.objects.filter(Q(author__icontains=query))
        else:
            results = Book.objects.filter(Q(title__icontains=query))

        if min_score:
            results = [result for result in results if result.avg_rating >= float(min_score)]
        if max_score:
            results = [result for result in results if result.avg_rating <= float(max_score)]

        if min_year:
            results = results.filter(pub_year__gte=int(min_year))
        if max_year:
            results = results.filter(pub_year__lte=int(max_year))

        sort_options = request.GET.get('sort-search')
        if sort_options == 'alphabetical':
            results = sorted(results, key=lambda book: book.title)
        elif sort_options == 'highest-rated':
            results = sorted(results, key=lambda book: book.avg_rating, reverse=True)
        elif sort_options == 'lowest-rated':
            results = sorted(results, key=lambda book: book.avg_rating)

    return render(request, 'books/search_results.html', {'form': form, 'results': results, 'query':query, 'field': field})

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
    book = None;

    if form.is_valid():
        query = form.cleaned_data['isbn']
        try:
            book = Book.objects.filter(isbn=query)[0]
        except:
            ol = OpenLibrary()

            edition = ol.Edition.get(isbn=query)
            if(edition):
                book = Book()
                book.title = edition.title;
                book.author = ', '.join(author_obj.name for author_obj in edition.authors)

                try:
                    work = ol.Work.get(edition.work_olid)
                    date = work.first_publish_date
                except:
                    date = edition.publish_date
                t = re.search('\d{% s}'% 4, date)
                book.pub_year = (int(t.group(0)) if t else None)
                book.olid = edition.olid

    context = {
        'form': form,
        'query_isbn': query,

        'book': book
    }

    return render(request, 'books/isbn.html', context)

def CreateFromIsbn(request):
    isbn = request.GET.get('isbn', "")
    try:
        book_obj = Book.objects.filter(isbn=isbn)[0]
    except:
        ol = OpenLibrary()
        edition = ol.Edition.get(isbn=isbn)
                
        try:
            work = ol.Work.get(edition.work_olid)
            date = work.first_publish_date
        except:
            date = edition.publish_date
        t = re.search('\d{% s}'% 4, date)
        pub_year = (int(t.group(0)) if t else None)

        book_obj = Book(title = edition.title, 
                        author = ', '.join(author_obj.name for author_obj in edition.authors),
                        isbn=isbn,
                        pub_year = pub_year,
                        olid=edition.olid)
        
        if edition.pages:
            book_obj.num_pages = edition.pages;

        book_obj.save()

    return redirect("books:view_book", book_id=book_obj.id)
