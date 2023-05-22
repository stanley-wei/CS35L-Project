from django import forms
from django.core.validators import MinValueValidator, MaxValueValidator

class ReviewForm(forms.Form):
    rating_choices = [(i, str(i)) for i in range(1,6)]  # Create a list of choices from 0 to 5
    rating = forms.ChoiceField(choices=rating_choices)

    text = forms.CharField(max_length=500);
    images = forms.ImageField(required=False);