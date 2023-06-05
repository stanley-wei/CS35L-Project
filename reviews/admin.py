from django.contrib import admin
from django.template.defaultfilters import escape
from django.urls import reverse
from django.utils.html import format_html

from .models import Review

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('book_link', 'user_link', 'rating', 'images')

    def book_link(self, review):
        return format_html('<a href="%s">%s</a>' % (reverse("admin:books_book_change", args=(review.book.id,)) , escape(review.book.title)))

    def user_link(self, review):
        return format_html('<a href="%s">%s</a>' % (reverse("admin:auth_user_change", args=(review.user.id,)) , escape(review.user)))
