from django.shortcuts import render
from rest_framework import generics,status
from .models import Room,CustomUser,Membership
from .serializers import RoomSerializer,CreateRoomSerializer,JoinRoomSerializer,CustomUserSerializer,LoginUserSerializer
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import JsonResponse
from django.contrib.auth.hashers import check_password

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
            print("room",room)
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
    serializer_class = JoinRoomSerializer

    def post(self, request, format=None):
        if not self.request.session.exists(self.request.session.session_key):
            self.request.session.create()
        code = request.data.get('code')
        if code:    
            room = Room.objects.filter(code=code).first()
            self.request.session['room_code'] = code
            if room:
                return Response(status=status.HTTP_200_OK)
            else:
                return Response({'error':'Invalid room code'},status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({'error':'Code is required'},status=status.HTTP_400_BAD_REQUEST) 
#Get user room
class getUserRoom(APIView):
    def get(self,request,format=None):
        if not self.request.session.exists(self.request.session.session_key):
            self.request.session.create()
        data = {
            'code':self.request.session.get('room_code')
        }
        return JsonResponse(data, status=status.HTTP_200_OK)
#Remove user from room
class removeUserFromRoom(APIView):
    def post(self,request,format=None):
        if self.request.session.exists(self.request.session.session_key):
            self.request.session['room_code'] = None
            return JsonResponse({'data':'success'},status=status.HTTP_200_OK)
        return JsonResponse({'error':'Unauthorized user'},status=status.HTTP_401_UNAUTHORIZED)             
        
          
            

    
