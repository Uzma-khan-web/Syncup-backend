from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect # <-- Ye add kiya
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    # Home page ko seedha API Docs par bhej rahe hain
    path('', lambda request: redirect('api/docs/', permanent=False)), 
    
    path('admin/', admin.site.urls),
    
    # Task API Endpoints
    path('api/', include('tasks.urls')),
    
    # JWT Authentication
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # Documentation (Note: Path changed to match your previous attempt)
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
]