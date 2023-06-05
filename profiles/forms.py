from django import forms

class ProfilePictureForm(forms.Form):
    profile_picture = forms.ImageField(label='Upload Profile Picture Here')