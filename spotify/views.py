from django.shortcuts import render,redirect
from rest_framework.views import APIView
from .credentilas import CLIENT_ID,CLIENT_SECRET,REDIRECT_URI
from rest_framework.response import Response
from rest_framework import status
from requests import Request, post
from .utils import update_or_create_user_tokens,is_spotify_authenticated
from rest_framework.response import Response



class AuthUrl(APIView):
    def get(self,request):
        scopes = 'user-read-playback-state user-modify-playback-state user-read-currently-playing'
        url = Request('GET','https://accounts.spotify.com/authorize',params={
            'scopes':scopes,
            'response_type':'code',
            'redirect_uri':REDIRECT_URI,
            'client_id':CLIENT_ID         
        }).prepare().url
        return Response({'url':url},status=status.HTTP_200_OK)

def spotify_callback(request):
    code = request.GET.get('code')
    error = request.GET.get('error') 
    print("error from spotify",error)
    print("code",code)
    current_user_id = request.session.get('current_user_id')
    response = post('https://accounts.spotify.com/api/token', data={
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': REDIRECT_URI,
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET
    }).json()
    print("the first response",response)
    print("the first response",response)
    access_token = response.get('access_token')
    token_type = response.get('token_type')
    refresh_token = response.get('refresh_token')
    expires_in = response.get('expires_in')
    error = response.get('error') 
    print("access token  in view",access_token)
    print("refresh token in view",refresh_token)
    print("token type in view",token_type)
    print("expires in in view",expires_in)
    update_or_create_user_tokens(current_user_id=current_user_id, access_token=access_token, token_type=token_type, expires_in=expires_in, refresh_token=refresh_token)
    current_room_code = request.session.get('current_room_code')
    print("current room",current_room_code)
    return redirect('frontend:eachRoom', roomCode=current_room_code)
class IsAuthenticated(APIView):
    def get(self,request,format=None):
        current_user_id = request.session.get('current_user_id')
        is_authenticated = is_spotify_authenticated(current_user_id)
        return Response({'status':is_authenticated},status=status.HTTP_200_OK)

 

        
    


