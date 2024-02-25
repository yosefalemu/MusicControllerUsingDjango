from django.db import models
from django.contrib.auth.models import User


class SpotifyToken(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,default=None)
    created_at = models.DateTimeField(auto_now_add=True)
    refresh_token = models.CharField(max_length=256)
    access_token = models.CharField(max_length=256)
    expires_in = models.DateTimeField()
    token_type = models.CharField(max_length=256)
