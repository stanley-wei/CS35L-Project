from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse

from reviews.models import Review

def profile(request, user_id):
    profile_user = User.objects.get(pk=user_id)
    signed_in_user = request.user
    if profile_user is not None:
        try:
            profile = UserProfile.objects.filter(user=profile_user)[0] 
        except:
            profile = UserProfile.objects.create(user=profile_user)
        
        reviews = Review.objects.filter(user=profile_user)
        context =  {
            'profile_user': profile_user,
            'reviews': reviews,
            'profile': profile,
            # 'signed_in_user': signed_in_user
        }
        if signed_in_user.is_authenticated:
            try: 
                signed_in_profile = UserProfile.objects.get(user=signed_in_user)
            except:
                signed_in_profile = UserProfile.objects.create(user=signed_in_user)
            context['signed_in_user'] = signed_in_profile
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
    if request.method == 'POST':
        form = ProfilePictureForm(request.POST, request.FILES)
        if form.is_valid():
            profile_user = UserProfile.objects.get(pk=user_id)
            profile_user.profile_picture = form.cleaned_data['profile_picture']
            profile_user.save()
            return HttpResponseRedirect(reverse("profiles:user-profile", args=(user_id,)))  # Redirect to the user's profile page
    else:
        form = ProfilePictureForm()
    return render(request, 'profiles/upload-profile-picture.html', {'form': form})

@login_required
def follow_user(request, user_id):
    friend_user = User.objects.get(pk=user_id)
    friend_profile = UserProfile.objects.get(user=friend_user)

    logged_in_user = request.user
    profile = UserProfile.objects.get(user=logged_in_user) 
    
    if friend_profile in profile.followed_users.all():
        profile.followed_users.remove(friend_profile)
    else:
        profile.followed_users.add(friend_profile)
    profile.save()
    return redirect("profiles:profile", user_id=user_id)