from django.urls import path

from . import views

app_name = "profiles"
urlpatterns = [
    path("signup", views.signup, name="signup"),
    path("login", views.login_user, name="login"),
]