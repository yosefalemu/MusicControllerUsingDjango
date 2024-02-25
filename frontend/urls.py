from django.urls import path
from .views import index

app_name = 'frontend'

urlpatterns = [
    path("", index, name="index"),
    path("login", index, name="login"),
    path("home", index, name="signup"),
    path("join",index, name="join"),
    path("create", index, name="create"),
    path("room/<str:roomCode>",index,name="eachRoom"),
    path("room/edit/<str:roomCode>",index,name="editroom")
]
