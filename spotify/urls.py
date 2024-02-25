from django.urls import path
from .views import AuthUrl,IsAuthenticated,spotify_callback

urlpatterns = [
    path('get-auth-url',AuthUrl.as_view(),name="GETAUTHURL"),
    path('redirect', spotify_callback),
    path('is-spotify-authenticated',IsAuthenticated.as_view(),name="ISSPOTIFYAUTHENTICATED")
]
