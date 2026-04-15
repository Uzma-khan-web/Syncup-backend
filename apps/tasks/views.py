import random
from rest_framework import viewsets, generics, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.contrib.auth.models import User
from django.core.mail import send_mail

# JWT Imports for Custom Response
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

from .models import Task, Project, SubTask, Profile
from .serializers import (
    TaskSerializer, ProjectSerializer, SubTaskSerializer, 
    UserRegistrationSerializer, ProfileSerializer
)

# --- CUSTOM JWT LOGIC ---
# Ye logic login ke waqt token ke saath username aur email bhejta hai
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        data['username'] = self.user.username
        data['email'] = self.user.email
        return data

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

# --- Authentication Logic (OTP & Register) ---
temp_otp_store = {}

@api_view(['POST'])
def send_otp(request):
    email = request.data.get('email')
    if not email:
        return Response({'error': 'Email is required!'}, status=status.HTTP_400_BAD_REQUEST)
    otp = str(random.randint(100000, 999999))
    temp_otp_store[email] = otp
    try:
        send_mail(
            'SyncUp Verification Code',
            f'Your code is: {otp}',
            None, [email], fail_silently=False,
        )
        return Response({'message': 'OTP sent!'}, status=status.HTTP_200_OK)
    except Exception:
        return Response({'error': 'Email failed!'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = [AllowAny]
    serializer_class = UserRegistrationSerializer

    def create(self, request, *args, **kwargs):
        email = request.data.get('email')
        user_otp = request.data.get('otp')
        if email not in temp_otp_store or temp_otp_store[email] != user_otp:
            return Response({'detail': 'Invalid OTP!'}, status=status.HTTP_400_BAD_REQUEST)
        response = super().create(request, *args, **kwargs)
        del temp_otp_store[email]
        return response

# --- Project Management Logic ---
class ProjectViewSet(viewsets.ModelViewSet):
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Project.objects.filter(created_by=self.request.user)

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Task.objects.filter(assigned_to=self.request.user)
        project_id = self.request.query_params.get('project_id')
        if project_id:
            queryset = queryset.filter(project_id=project_id)
        return queryset

    def perform_create(self, serializer):
        serializer.save(assigned_to=self.request.user)

class SubTaskViewSet(viewsets.ModelViewSet):
    serializer_class = SubTaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return SubTask.objects.filter(task__assigned_to=self.request.user)
    
class ProfileViewSet(viewsets.ModelViewSet):
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Hum sirf current logged-in user ki profile chahte hain
        return Profile.objects.filter(user=self.request.user)

    def list(self, request, *args, **kwargs):
        # Ye part check karega ki profile bani hai ya nahi
        profile, created = Profile.objects.get_or_create(user=request.user)
        
        # Hum direct object bhejenge list ki jagah, taaki frontend ko asani ho
        serializer = self.get_serializer(profile)
        return Response(serializer.data)