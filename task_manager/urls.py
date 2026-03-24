from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path, include

from project.views import register_user

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("project.urls", namespace="project")),
    path("accounts/login/", LoginView.as_view(), name="login"),
    path("accounts/logout/", LogoutView.as_view(), name="logout"),
    path("accounts/register/", register_user, name="register"),
]
