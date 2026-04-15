from rest_framework import serializers
from .models import Task, Project, SubTask, Profile
from django.contrib.auth.models import User

# --- User Serializers ---
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = ['username', 'password', 'email']

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password']
        )
        return user

# --- Project Serializer ---
class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['id', 'name', 'description', 'created_at', 'created_by']
        read_only_fields = ['id', 'created_at', 'created_by']

# --- SubTask Serializer ---
class SubTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubTask
        fields = ['id', 'title', 'is_completed']

# --- Task Serializer ---
class TaskSerializer(serializers.ModelSerializer):
    assigned_to_details = UserSerializer(source='assigned_to', read_only=True)
    project_details = ProjectSerializer(source='project', read_only=True)
    subtasks = SubTaskSerializer(many=True, read_only=True)
    
    class Meta:
        model = Task
        fields = [
            'id', 'project', 'project_details', 'title', 'description', 
            'status', 'priority', 'assigned_to', 'assigned_to_details', 
            'subtasks', 'due_date', 'created_at'
        ]
        read_only_fields = ['id', 'created_at', 'assigned_to']

# --- Profile Serializer ---
class ProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    email = serializers.EmailField(source='user.email', read_only=True)

    class Meta:
        model = Profile
        fields = ['username', 'email', 'bio', 'profile_pic', 'location']