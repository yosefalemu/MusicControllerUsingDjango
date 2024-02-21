from django.shortcuts import render
from rest_framework import generics,status
from .models import Room,CustomUser,Membership
from .serializers import RoomSerializer,CreateRoomSerializer,CustomUserSerializer,LoginUserSerializer,CustomUserSerializer,EditUserSerializer
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import JsonResponse
from django.contrib.auth.hashers import check_password
from django.utils import timezone

# Default List Api Views
class RoomView(generics.ListAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
#create user
class CreateUser(APIView):
    parser_classes = (MultiPartParser, FormParser)
    serializer_class = CustomUserSerializer
    def post(self, request,):
        if not self.request.session.exists(self.request.session.session_key):
            self.request.session.create()
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data.get('email')
            username = serializer.validated_data.get('username')
            if CustomUser.objects.filter(username=username).exists():
                return JsonResponse({'error':'Username is taken'},status=status.HTTP_400_BAD_REQUEST)
            if CustomUser.objects.filter(email=email).exists():
                return JsonResponse({'error':'Email taken'},status=status.HTTP_400_BAD_REQUEST)
            user = serializer.save()  
            return JsonResponse(CustomUserSerializer(user).data, status=status.HTTP_200_OK)
        else:   
            return JsonResponse({'error': 'invalid input'}, status=status.HTTP_400_BAD_REQUEST)
# Login user
class LoginUser(APIView):
    serializer_class = LoginUserSerializer
    def post(self, request):
        data_from_frontend = request.data.get('data', {})
        serializer = self.serializer_class(data=data_from_frontend)
        
        if serializer.is_valid():
            email = serializer.validated_data.get("email")
            password = serializer.validated_data.get("password")
            
            user = CustomUser.objects.filter(email=email).first()
            print("user login",user)
            rooms = user.room_set.all()
            print("all rooms",rooms)
            if user:
                if check_password(password, user.password):
                    print("Password correct")
                    return Response(CustomUserSerializer(user).data,status=status.HTTP_200_OK)
                else:
                    print("Invalid password")
                    return JsonResponse({'error': 'Invalid password'}, status=status.HTTP_400_BAD_REQUEST)
            else:
                print("Email not registered")
                return JsonResponse({'error': 'Email is not registered'}, status=status.HTTP_404_NOT_FOUND)
        else:
            print(serializer.errors)
            return JsonResponse({'error': 'Invalid email'}, status=status.HTTP_400_BAD_REQUEST)     
     
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
            user = CustomUser.objects.filter(id=id).first()
            print("room found with that code",room)
            print("user found with that id",user)
            if room:
                if user:
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
                return Response({'error':'Invalid room code'},status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({'error':'Code is required'},status=status.HTTP_400_BAD_REQUEST) 
#Get user room
class getUserRoom(APIView):
    def get(self,request,format=None):
        id = request.GET.get('id')
        print("the user id",id)
        if not self.request.session.exists(self.request.session.session_key):
            self.request.session.create()
        user = CustomUser.objects.filter(id=id).first()
        print("user",user)
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
        user = CustomUser.objects.filter(id=user_id).first()
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
        
                     
        
          
            

    
