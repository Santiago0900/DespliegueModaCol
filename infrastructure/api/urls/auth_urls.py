from django.urls import path
from infrastructure.api.views.auth_views import (
    login_view,
    logout_view,
    home_view,
    forgot_password_view,
    reset_password_view,
)

urlpatterns = [
    path("", home_view, name="home"),
    path("login", login_view, name="login"),
    path("logout", logout_view, name="logout"),
    path("forgot-password", forgot_password_view, name="forgot_password"),
    path("reset-password/<str:token>", reset_password_view, name="reset_password"),
]