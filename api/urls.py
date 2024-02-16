from django.urls import path
from . import views

urlpatterns = [
    path("rooms/",views.RoomView.as_view(),name="RoomView"),
    path("create-room/",views.CreateRoom.as_view(),name="CreateRoom")
]
