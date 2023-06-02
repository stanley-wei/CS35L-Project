from django.urls import path

from . import views

app_name = "users"
urlpatterns = [
    path("signup", views.signup, name="signup"),
    path("login", views.login_user, name="login"),
    path("forget-password", views.CustomPasswordResetView.as_view(), name="forget_password"),
]