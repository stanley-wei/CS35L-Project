from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse

from books.models import Book
from .forms import ReviewForm
from .models import Review

@login_required
def MakeReview(request, book_id):
    # if this is a POST request we need to process the form data
    if request.method == "POST":
        # create a form instance and populate it with data from the request:
        form = ReviewForm(request.POST)

        # check whether it's valid:
        if form.is_valid():
            past_reviews = Review.objects.filter(user=request.user, book_id=book_id)
            if past_reviews is not None:
                past_reviews.delete()

            review = Review(user=request.user, book=Book.objects.get(pk=book_id), rating=form.cleaned_data["rating"], text=form.cleaned_data["text"])
            review.save()
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            return HttpResponseRedirect(reverse("books:view_book", args=(book_id,)))

    # if a GET (or any other method) we'll create a blank form
    else:
        form = ReviewForm()

    return render(request, "reviews/review_book.html", {"form": form, "book": Book.objects.get(pk=book_id)})

@login_required
def EditReview(request, book_id):
    review = Review.objects.filter(user=request.user, book__id=book_id)[0]
    if request.method == "POST":
        form = ReviewForm(request.POST)

        if form.is_valid():
            review.rating = form.cleaned_data["rating"]
            review.text = form.cleaned_data["text"]
            review.save()

            return HttpResponseRedirect(reverse("books:view_book", args=(book_id,)))
    else:
        form = ReviewForm(initial={"rating": review.rating, "text": review.text})

    return render(request, "reviews/review_book.html", {"form": form, "book": Book.objects.get(pk=book_id)})
