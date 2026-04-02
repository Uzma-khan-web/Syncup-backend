from rest_framework import serializers
from .models import Task
from django.contrib.auth.models import User

# 1. For viewing user info (Keep this as is)
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

# 2. NEW: For creating new users (Registration)
class UserRegistrationSerializer(serializers.ModelSerializer):
    # We want the password to be write-only so it never shows up in GET responses
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'password', 'email']

    def create(self, validated_data):
        # Use create_user so Django hashes the password (encrypts it)
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password']
        )
        return user

# 3. For Tasks (Keep this as is)
class TaskSerializer(serializers.ModelSerializer):
    assigned_to_details = UserSerializer(source='assigned_to', read_only=True)

    class Meta:
        model = Task
        fields = [
            'id', 'title', 'description', 'status', 
            'priority', 'assigned_to', 'assigned_to_details', 
            'created_at', 'due_date'
        ]
        read_only_fields = ['id', 'created_at', 'assigned_to']