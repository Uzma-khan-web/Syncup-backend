from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView # Refresh token ke liye
from .views import (
    TaskViewSet, 
    ProjectViewSet, 
    SubTaskViewSet, 
    ProfileViewSet,
    RegisterView, 
    send_otp,
    MyTokenObtainPairView  # <--- 1. Apna custom view import karein
)

# Router setup
router = DefaultRouter()
router.register(r'tasks', TaskViewSet, basename='task')
router.register(r'projects', ProjectViewSet, basename='project')
router.register(r'subtasks', SubTaskViewSet, basename='subtask')
router.register(r'profile', ProfileViewSet, basename='profile')

urlpatterns = [
    # Router ke saare endpoints (tasks, projects, subtasks, profile)
    path('', include(router.urls)),
    
    # --- UPDATED AUTH ENDPOINTS ---
    # Default 'TokenObtainPairView' ki jagah apna 'MyTokenObtainPairView' use karein
    path('token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # Registration & OTP
    path('register/', RegisterView.as_view(), name='register'),
    path('send-otp/', send_otp, name='send_otp'),
]