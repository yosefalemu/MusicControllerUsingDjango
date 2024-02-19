from django.shortcuts import render
from rest_framework import generics,status
from .models import Room,CustomUser
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
            # Save the user instance  
            user = serializer.save()
            print("user created",user)  
            return JsonResponse({'message': 'User created successfully'}, status=status.HTTP_200_OK)
        else:   
            return JsonResponse({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
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
            
            if user:
                if check_password(password, user.password):
                    print("Password correct")
                    return JsonResponse({'message': 'Login successfully'}, status=status.HTTP_200_OK)
                else:
                    print("Invalid password")
                    return JsonResponse({'error': 'Invalid password'}, status=status.HTTP_400_BAD_REQUEST)
            else:
                print("Email not registered")
                return JsonResponse({'error': 'Email is not registered'}, status=status.HTTP_404_NOT_FOUND)
        else:
            print(serializer.errors)
            return JsonResponse({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)     
     
# Create Room    
class CreateRoom(APIView):
    serializer_class = CreateRoomSerializer
    def post(self,request):
        if not self.request.session.exists(self.request.session.session_key):
            self.request.session.create()
        data_from_frontend = request.data.get('data', {})
        serializer = self.serializer_class(data=data_from_frontend)
        if serializer.is_valid():
            guest_can_pause = serializer.data.get('guest_can_pause')
            votes_to_skip = serializer.data.get('votes_to_skip')
            host = self.request.session.session_key
            queryset = Room.objects.filter(host=host)
            if queryset.exists():
                room = queryset[0]
                room.guest_can_pause = guest_can_pause
                room.votes_to_skip = votes_to_skip
                room.save(update_fields=['guest_can_pause','votes_to_skip'])
                return Response(RoomSerializer(room).data,status=status.HTTP_200_OK)
            else:
                room = Room(host=host,guest_can_pause=guest_can_pause,votes_to_skip=votes_to_skip)
                room.save()
                return Response(RoomSerializer(room).data,status=status.HTTP_201_CREATED)
        return Response({'Bad Request':'Invalid data'},status=status.HTTP_400_BAD_REQUEST)
 
#Get Room
class GetRoom(APIView):
    serializer_class = RoomSerializer
    lookup_url_kwarg = 'code'

    def get(self, request, format=None):
        code = request.GET.get(self.lookup_url_kwarg)
        if code != None:
            room = Room.objects.filter(code=code)
            if len(room) > 0:
                data = RoomSerializer(room[0]).data
                data['is_host'] = self.request.session.session_key == room[0].host
                return Response(data, status=status.HTTP_200_OK)
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
        
          
            

    
