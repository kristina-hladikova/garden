from django.urls import path
# from . import views
from .views import homepage, RegistrationView, LoginView, LogoutView, MyChangePasswordView, garden_detail, garden, \
    update_garden, delete_garden, contact, MembershipView, create_garden
from .views_plants import vegetable, fruit, herbs, fruit_tree

urlpatterns = [
    path("", homepage, name="homepage"),
    path("register/", RegistrationView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("change_password/", MyChangePasswordView.as_view(), name="change_password"),
    # path("change_password/done", MyPasswordResetDoneView.as_view(), name="password_done"),
    path("garden/", garden, name="garden"),
    path("garden/<int:garden_id>/", garden_detail, name="garden_detail"),
    path("create_garden/", create_garden, name="create_garden"),
    path("garden/<int:garden_id>/update_garden/", update_garden, name="update_garden"),
    path("garden/<int:garden_id>/delete_garden/", delete_garden, name="delete_garden"),
    path("contact", contact, name="contact"),
    path('membership/', MembershipView.as_view(), name='membership'),
    path('vegetable/', vegetable, name='vegetable'),
    path('fruit/', fruit, name='fruit'),
    path('herbs/', herbs, name='herbs'),
    path('fruit_tree/', fruit_tree, name='fruit_tree'),
]