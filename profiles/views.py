from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse

from reviews.models import Review
from profiles.models import UserProfile
from .forms import ProfilePictureForm

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
        followed_fav_books = set()
        for followed_user in profile.followed_users.all():
            for book in followed_user.favorite_books.all():
                if book not in followed_fav_books:
                    followed_fav_books.add(book)
        context =  {
            'profile_user': profile_user,
            'reviews': reviews,
            'profile': profile,
            'followed_fav_books': followed_fav_books,
        }
        return render(request, 'profiles/user-profile.html', context)
    return None

@login_required
def upload_profile_picture(request, user_id):
    if request.method == 'POST':
        form = ProfilePictureForm(request.POST, request.FILES)
        if form.is_valid():
            user = User.objects.get(pk=user_id)
            profile_user = UserProfile.objects.get(user=user) 
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
        friend_profile.follower_users.remove(profile)
    else:
        profile.followed_users.add(friend_profile)
        friend_profile.follower_users.add(profile)
    profile.save()
    friend_profile.save()
    return redirect("profiles:profile", user_id=user_id)