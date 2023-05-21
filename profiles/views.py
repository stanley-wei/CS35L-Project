from django.contrib.auth.models import User
from django.shortcuts import render

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
        reviews = Review.objects.filter(user=profile_user)
        context =  {
            'profile_user': profile_user,
            'reviews': reviews
        }
        return render(request, 'profiles/user-profile.html', context)
    return None