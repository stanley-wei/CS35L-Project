from django import forms

class BookSearchForm(forms.Form):
    query = forms.CharField(label='Search')