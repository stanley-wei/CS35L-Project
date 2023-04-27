from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from books.models import Book
from .forms import ReviewForm
from .models import Review

def MakeReview(request, book_id):
    # if this is a POST request we need to process the form data
    if request.method == "POST":
        # create a form instance and populate it with data from the request:
        form = ReviewForm(request.POST)

        # check whether it's valid:
        if form.is_valid():
            review = Review(user=request.user, book=Book.objects.get(pk=book_id), rating=form.cleaned_data["rating"], text=form.cleaned_data["text"])
            review.save()
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            return HttpResponseRedirect(reverse("book", args=(book_id,)))

    # if a GET (or any other method) we'll create a blank form
    else:
        form = ReviewForm()

    return render(request, "reviews/review_book.html", {"form": form, "book": book_id})