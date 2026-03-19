from django.urls import path
from project.views import index

app_name = "project"

urlpatterns = [
    path("", index, name="index"),
]