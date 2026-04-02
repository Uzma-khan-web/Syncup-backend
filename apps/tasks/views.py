from rest_framework import viewsets, permissions, generics, filters # Added generics
from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.auth.models import User # Added User model
from .models import Task
from .serializers import TaskSerializer, UserRegistrationSerializer # Added UserRegistrationSerializer

# 1. THE TASK VIEWSET (Your existing code)
class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'priority']
    search_fields = ['title', 'description']
    ordering_fields = ['created_at', 'due_date']

    def get_queryset(self):
        return Task.objects.filter(assigned_to=self.request.user)

    def perform_create(self, serializer):
        serializer.save(assigned_to=self.request.user)


# 2. THE REGISTER VIEW (Add this now)
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    # This is crucial: Anyone must be able to access this to sign up!
    permission_classes = [permissions.AllowAny]