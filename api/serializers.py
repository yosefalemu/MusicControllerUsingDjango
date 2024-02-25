from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from .models import Room,CustomUser

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','first_name', 'last_name', 'username', 'email', 'password']
class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['profile_picture']
 

class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ["id","code","host","guest_can_pause","votes_to_skip","created_at","members"]
class CreateRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ["guest_can_pause","votes_to_skip","host","members"]
        
class JoinRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ["code"]

class LoginUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'password']
class EditUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ['id','guest_can_pause','votes_to_skip']
    
    
