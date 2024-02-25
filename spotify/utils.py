import base64
from django.utils import timezone
from datetime import timedelta
from .models import SpotifyToken
from django.contrib.auth.models import User
from requests import post
from .credentilas import CLIENT_ID,CLIENT_SECRET

def get_user_tokens(current_user_id):
    user_token = SpotifyToken.objects.filter(user_id = current_user_id).first()
    print("current user found",user_token)
    print("current user found",user_token)
    if user_token:
        return user_token
    else:
        return None
import requests

# def refresh_token(current_user_id):
#     refresh_token = get_user_tokens(current_user_id).refresh_token
#     auth_options = {
#         'url': 'https://accounts.spotify.com/api/token',
#         'headers': {
#             'content-type': 'application/x-www-form-urlencoded',
#             'Authorization': 'Basic ' + base64.b64encode(bytes(CLIENT_ID + ':' + CLIENT_SECRET, 'utf-8')).decode('utf-8')
#         },
#         'data': {
#             'grant_type': 'refresh_token',
#             'refresh_token': refresh_token
#         }
#     }

#     response = requests.post(auth_options['url'], headers=auth_options['headers'], data=auth_options['data'])

#     if response.status_code == 200:
#         data = response.json()
#         print("response that found",response)
#         print("done")
#         access_token = data.get('access_token')
#         refresh_token = data.get('refresh_token')
#         token_type = data.get('token_type')
#         expires_in = data.get('expires_in')
#         refresh_token = data.get('refresh_token')
#         print("current user in refresh token",current_user_id)
#         print("access token in refresh token",access_token)
#         print("refresh token in refresh token",refresh_token)
#         print("token type in refresh token",token_type)
#         print("expires in in refresh token",expires_in)
        
        


    
def refresh_token(current_user_id):
    refresh_token = get_user_tokens(current_user_id).refresh_token
    print("refresh token that found",refresh_token)
    print("refresh token that found",refresh_token)
    print("refresh token that found",refresh_token)
    response = post('https://accounts.spotify.com/api/token', data={
        'grant_type': 'refresh_token',
        'refresh_token': refresh_token,
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET
    }).json()
    print("in refresh token",response)
    print("in refresh token",response)
    access_token = response.get('access_token')
    token_type = response.get('token_type')
    expires_in = response.get('expires_in')
    print("current user in refresh token",current_user_id)
    print("access token in refresh token",access_token)
    print("refresh token in refresh token",refresh_token)
    print("token type in refresh token",token_type)
    print("expires in in refresh token",expires_in)
    update_or_create_user_tokens(current_user_id=current_user_id,access_token=access_token,token_type=token_type,expires_in=expires_in,refresh_token=refresh_token)
    
    
def update_or_create_user_tokens(current_user_id,access_token,refresh_token, token_type ,expires_in):
    print("current user",current_user_id)
    print("access token",access_token)
    print("refresh token",refresh_token)
    print("token type",token_type)
    print("expires in",expires_in)
    user_token = get_user_tokens(current_user_id)
    expires_in = timezone.now() + timedelta(seconds=expires_in)
    if user_token:
        user_token.access_token = access_token
        user_token.refresh_token = refresh_token
        user_token.expires_in = expires_in
        user_token.token_type = token_type
        user_token.save(update_fields=['access_token','refresh_token','token_type','expires_in'])
    else:
        user = User.objects.filter(id = current_user_id).first()
        user_token = SpotifyToken(user=user,access_token = access_token,refresh_token = refresh_token,token_type=token_type,expires_in=expires_in)
        user_token.save()
def is_spotify_authenticated(current_user_id):
    current_user = get_user_tokens(current_user_id)
    if current_user:
        expiry_data = current_user.expires_in
        if expiry_data <= timezone.now():
            refresh_token(current_user_id)
        return True
    return False 
            
     