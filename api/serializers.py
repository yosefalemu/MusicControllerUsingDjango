from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from .models import Room,CustomUser

class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ["id","code","host","guest_can_pause","votes_to_skip","created_at"]
class CreateRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ["guest_can_pause","votes_to_skip"]
class JoinRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ["code"]


class CustomUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'username', 'email', 'password','profile_picture']
    def create(self, validated_data):
        password = validated_data.pop('password')
        validated_data['password'] = make_password(password)
        return CustomUser.objects.create(**validated_data)
class LoginUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    class Meta:
        model = CustomUser
        fields = ['email', 'password']
    
    
