from django import forms
from django.core.validators import MinValueValidator, MaxValueValidator

class ReviewForm(forms.Form):
    rating_choices = [(i, str(i)) for i in range(1, 6)]  # Create a list of choices from 1 to 5
    rating = forms.ChoiceField(choices=rating_choices, widget=forms.Select(attrs={'class': 'custom-select'}))

    text = forms.CharField(max_length=500, widget=forms.Textarea(attrs={'class': 'custom-textarea'}))
    images = forms.ImageField(required=False, widget=forms.ClearableFileInput(attrs={'class': 'custom-file-input'}))
