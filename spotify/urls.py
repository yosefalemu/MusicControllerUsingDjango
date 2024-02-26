from django.urls import path
from .views import AuthUrl,IsAuthenticated,spotify_callback,GetSeveralAlbum

urlpatterns = [
    path('get-auth-url',AuthUrl.as_view(),name="GETAUTHURL"),
    path('redirect', spotify_callback),
    path('is-spotify-authenticated',IsAuthenticated.as_view(),name="ISSPOTIFYAUTHENTICATED"),
    path('get-several-album/',GetSeveralAlbum.as_view(),name="GETSEVERALALBUM")
]
