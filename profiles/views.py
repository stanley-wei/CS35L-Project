from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse

from reviews.models import Review

def profile(request, user_id):
    profile_user = User.objects.get(pk=user_id)
    if profile_user is not None:
        reviews = Review.objects.filter(user=profile_user)
        context =  {
            'profile_user': profile_user,
            'reviews': reviews
        }
        return render(request, 'profiles/profile.html', context)
    return None

def user_profile(request, user_id):
    profile_user = User.objects.get(pk=user_id)
    if profile_user is not None:
        try:
            profile = UserProfile.objects.filter(user=profile_user)[0] 
        except:
            profile = UserProfile.objects.create(user=profile_user)
            
        reviews = Review.objects.filter(user=profile_user)
        context =  {
            'profile_user': profile_user,
            'reviews': reviews,
            'profile': profile
        }
        return render(request, 'profiles/user-profile.html', context)
    return None

from django import forms
from profiles.models import UserProfile

class ProfilePictureForm(forms.Form):
    profile_picture = forms.ImageField()

def upload_profile_picture(request, user_id):
    user = User.objects.get(pk=user_id)
    if request.method == 'POST':
        form = ProfilePictureForm(request.POST, request.FILES)
        if form.is_valid():
            profile_user = UserProfile.objects.get(user=user)
            profile_user.profile_picture = form.cleaned_data['profile_picture']
            profile_user.save()
            return HttpResponseRedirect(reverse("profiles:user-profile", args=(user_id,)))  # Redirect to the user's profile page
    else:
        form = ProfilePictureForm()
    return render(request, 'profiles/upload-profile-picture.html', {'form': form})