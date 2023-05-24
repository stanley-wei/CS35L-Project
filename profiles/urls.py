from django.urls import path

from . import views

app_name = "profiles"
urlpatterns = [
    path("<int:user_id>/", views.profile, name="profile"),
    path("<int:user_id>/page", views.user_profile, name="user-profile"),
    path('<int:user_id>/upload-profile-picture/', views.upload_profile_picture, name='upload_profile_picture'),
]