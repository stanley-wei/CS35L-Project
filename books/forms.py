from django import forms

class BookSearchForm(forms.Form):
    query = forms.CharField(label='Search')

class IsbnSearchForm(forms.Form):
    isbn = forms.CharField(label='Enter ISBN here')
