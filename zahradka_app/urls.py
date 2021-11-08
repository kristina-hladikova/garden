from django.urls import path
from . import views
from .views import RegistrationView, LoginView, LogoutView, ChangePasswordView, garden_detail

urlpatterns = [
    path("", views.homepage, name="homepage"),
    path("register/", RegistrationView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("change_password/", ChangePasswordView.as_view(), name="change_password"),
    path("garden/<int:pk>", garden_detail, name="garden"),
]