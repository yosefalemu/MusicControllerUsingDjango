from django.urls import path
from .views import index

urlpatterns = [
    path("", index, name="index"),
    path("login", index, name="login"),
    path("join",index, name="join"),
    path("create", index, name="create")
]
