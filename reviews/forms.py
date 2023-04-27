from django import forms

class ReviewForm(forms.Form):
    rating = forms.IntegerField()
    text = forms.CharField(max_length=500);