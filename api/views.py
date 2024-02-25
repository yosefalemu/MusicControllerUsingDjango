from django.shortcuts import render
from rest_framework import generics,status
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login
from django.contrib.auth.hashers import check_password
from .models import Room,CustomUser,Membership
from .serializers import UserSerializer,CustomUserSerializer,LoginUserSerializer,CreateRoomSerializer,RoomSerializer,EditUserSerializer
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import JsonResponse
from django.contrib.auth.hashers import check_password
from django.utils import timezone
from django.contrib.auth.mixins import LoginRequiredMixin

# Default List Api Views
class RoomView(generics.ListAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
#create user
from django.http import JsonResponse
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.views import APIView
from .serializers import UserSerializer, CustomUserSerializer
from django.contrib.auth.models import User

class CreateUser(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request):
        if not self.request.session.exists(self.request.session.session_key):
            self.request.session.create()

        user_serializer = UserSerializer(data=request.data)
        custom_user_serializer = CustomUserSerializer(data=request.data)

        if user_serializer.is_valid():
            if custom_user_serializer.is_valid():             
                # user_instance = user_serializer
                # custom_user_instance = custom_user_serializer.save(user=user_instance)
                user_data = user_serializer.validated_data
                first_name = user_serializer.validated_data.get('first_name')
                last_name = user_serializer.validated_data.get('last_name')
                username = user_serializer.validated_data.get('username')
                email = user_serializer.validated_data.get('email')
                password = user_serializer.validated_data.get('password')
                if len(first_name) < 3:
                    return JsonResponse({'first_name':'First name should be atleast 3 characters'},status=status.HTTP_400_BAD_REQUEST)
                if len(last_name) < 3:
                    return JsonResponse({'last_name':'Last name should be atleast 3 characters'},status=status.HTTP_400_BAD_REQUEST) 
                if len(username) < 3:
                    return JsonResponse({'username':'Username should be atleast 3 characters'},status=status.HTTP_400_BAD_REQUEST) 
                if len(password) < 6:
                    return JsonResponse({'password':'Password should be atleast 6 characters'},status=status.HTTP_400_BAD_REQUEST)              
                if User.objects.filter(email = email).first():
                    return JsonResponse({'email':'Email is taken'},status=status.HTTP_400_BAD_REQUEST)
                user_instance = User.objects.create_user(first_name = user_data['first_name'],last_name = user_data['last_name'],username = user_data['username'],email = user_data['email'],password = user_data['password'])
                print("user instance to be created",user_instance)
                custom_user_instance  = custom_user_serializer.save(user = user_instance)
                print("custom user instance to be created",custom_user_instance)
                response_data = {
                    'user': UserSerializer(user_instance).data,
                    'custom_user': CustomUserSerializer(custom_user_instance).data
                }

                return JsonResponse(response_data, status=status.HTTP_200_OK)
            else:
                return JsonResponse(custom_user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return JsonResponse(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Login user
class LoginUser(APIView):
    serializer_class = LoginUserSerializer

    def post(self, request):
        print("Data from frontend:", request.data)
        serializer = self.serializer_class(data=request.data.get('data', {}))
        
        if serializer.is_valid():
            print("Serializer is valid")
            email = serializer.validated_data.get("email")
            password = serializer.validated_data.get("password")
            user = User.objects.filter(email=email).first()
            if user:
                if check_password(password, user.password):
                    user_authenticated = authenticate(request, username=user, password=password)
                    request.user = user_authenticated
                    print("user authenticated",user_authenticated)
                    log_in_user = login(request, user)
                    print("logged in user",log_in_user)
                    request.session['current_user_id'] = user_authenticated.id
                    custom_user = CustomUser.objects.filter(user=user).first()
                    response_data = {
                        'user': UserSerializer(user).data,
                        'custom_user': CustomUserSerializer(custom_user).data
                    }
                    return Response(response_data, status=status.HTTP_200_OK)
                else:
                    print("Authentication failed.")
                    return Response({'password': 'Invalid password'}, status=status.HTTP_404_NOT_FOUND)
            else:
                print("User not found.")
                return Response({'email': 'Invalid email'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            print("Serializer errors:", serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
     
# Create Room    
class CreateRoom(APIView):
    serializer_class = CreateRoomSerializer
    def post(self,request):
        if not self.request.session.exists(self.request.session.session_key):
            self.request.session.create()
        data_from_frontend = request.data.get('data', {})
        serializer = self.serializer_class(data=data_from_frontend)
        print("serializer",serializer)
        if serializer.is_valid():
            host = serializer.validated_data.get('host')
            print("host",host)
            room = serializer.save()
            print("user to create",host)
            print("room to be created",room)
            Membership.objects.create(user=host,room=room)
            return JsonResponse(RoomSerializer(room).data,status=status.HTTP_201_CREATED)
        return JsonResponse({'error':serializer.errors},status=status.HTTP_400_BAD_REQUEST)
 
#Get Room
class GetRoom(APIView):
    serializer_class = RoomSerializer
    def get(self, request, format=None):
        code = request.GET.get('code')
        id = int(request.GET.get('id'))
        if code != None:
            room = Room.objects.filter(code=code).first()
            if room:
                members = room.members.all()
                print("all members",members)
                room = RoomSerializer(room).data
                room['is_host'] = room["host"] == id
                return Response(room, status=status.HTTP_200_OK)
            return Response({'Room Not Found': 'Invalid Room Code.'}, status=status.HTTP_404_NOT_FOUND)

        return Response({'Bad Request': 'Code paramater not found in request'}, status=status.HTTP_400_BAD_REQUEST)
#Join room
class JoinRoom(APIView):
    lookup_url_kwarg = 'code'
    def post(self, request, format=None):
        if not self.request.session.exists(self.request.session.session_key):
            self.request.session.create()
        code = request.data.get('code')
        id = request.data.get('id')
        print("code from frontend",code)
        print("id from frontend",id)
        if code:    
            room = Room.objects.filter(code=code).first()
            user = User.objects.filter(id=id).first()
            print("room found with that code",room)
            print("user found with that id",user)
            if room:
                if user:
                    request.session['current_room_code'] = code
                    if Membership.objects.filter(user=user,room=room).exists():
                        print("User exist in the rooms")
                        return JsonResponse({'messages': 'User already in this room'}, status=status.HTTP_200_OK)
                    print("user were added to this room")
                    room.members.add(user,through_defaults={"date_joined":timezone.now()})
                    # Membership.objects.create(user=user,room=room)
                    return JsonResponse({'messages':'User join room successfully'},status=status.HTTP_200_OK)   
                else:
                    return JsonResponse({'error':'invalid credential'},status=status.HTTP_404_NOT_FOUND)
            else:
                return JsonResponse({'error':'Invalid room code'},status=status.HTTP_404_NOT_FOUND)
        else:
            return JsonResponse({'error':'Code is required'},status=status.HTTP_400_BAD_REQUEST) 
#Get user room
class getUserRoom(APIView):
    def get(self,request,format=None):
        id = request.GET.get('id')
        current_user_id = request.session.get('current_user_id')
        print("current_user",current_user_id)
        print("current_user",current_user_id)
        print("current_user",current_user_id)
        if not self.request.session.exists(self.request.session.session_key):
            self.request.session.create()
        user = User.objects.filter(id=id).first()
        if user:
            user_rooms = Room.objects.filter(members__id=id)
            print("user rooms",user_rooms)
            room_serializer = RoomSerializer(user_rooms, many=True)
            print("room serializers",room_serializer)
            return JsonResponse({'message':room_serializer.data}, status=status.HTTP_200_OK)
        return JsonResponse({'error':'user not found'}, status=status.HTTP_404_NOT_FOUND)

#Remove user from room
class removeUserFromRoom(APIView):
    def post(self,request,format=None):
        if not self.request.session.exists(self.request.session.session_key):
            self.request.session.create()
        is_host = request.data.get('is_host')
        room_id = request.data.get('room_id')
        user_id = request.data.get('user_id')
        print("is host",is_host)
        print("room id",room_id)
        print("user id",user_id)
        user = User.objects.filter(id=user_id).first()
        room = Room.objects.filter(id=room_id).first()
        print("user removed",user)
        print("room from",room)
        if room:
            if user:
                if is_host:
                    room.members.clear()
                    room.delete()
                    return JsonResponse({'message':'User removed and room deleted'},status=status.HTTP_200_OK)
                else:
                    room.members.remove(user)
                    return JsonResponse({'message':'User removed from room successfully'},status=status.HTTP_200_OK)
            return JsonResponse({'error':'User not found'},status=status.HTTP_404_NOT_FOUND)
        return JsonResponse({'error':'Room not found'},status=status.HTTP_404_NOT_FOUND)
#Edit room
class editRoom(APIView):
    def patch(self,request,format=None):
        if not self.request.session.exists(self.request.session.session_key):
            self.request.session.create()
        data_from_frontend = request.data.get('data', {})      
        serializer = EditUserSerializer(data=data_from_frontend)
        if serializer.is_valid():
            room_id = data_from_frontend.get('id')
            guest_can_pause = serializer.validated_data.get('guest_can_pause')
            votes_to_skip = serializer.validated_data.get('votes_to_skip')
            room = Room.objects.filter(id=room_id).first()
            if room:
                room.guest_can_pause = guest_can_pause
                room.votes_to_skip = votes_to_skip
                room.save(update_fields=['guest_can_pause','votes_to_skip'])
                return JsonResponse(RoomSerializer(room).data,status=status.HTTP_200_OK)     
            return JsonResponse({'error':'Invalid room id'},status=status.HTTP_404_NOT_FOUND)
        return JsonResponse({'error':'Not valid data'},status=status.HTTP_400_BAD_REQUEST)
        
                     
        
          
            

    
