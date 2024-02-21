from django.urls import path
from . import views

urlpatterns = [
    path("signup/",views.CreateUser.as_view(),name="CreateUser"),
    path("login/",views.LoginUser.as_view(),name="LoginUser"),
    path("rooms/", views.RoomView.as_view(), name="RoomView"),
    path("create-room/", views.CreateRoom.as_view(), name="CreateRoom"),
    path("get-room/", views.GetRoom.as_view(), name="GetRoom"),
    path("join-room/",views.JoinRoom.as_view(),name="joinRoom"),
    path("get-user-room/",views.getUserRoom.as_view(),name="getUserRoom"),
    path("remove-user-from-room/",views.removeUserFromRoom.as_view(),name="RemoveUserFromRoom"),
    path("edit-room/",views.editRoom.as_view(),name="EditRoom")
]
