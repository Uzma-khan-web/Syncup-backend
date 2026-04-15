from django.db import models
from django.contrib.auth.models import User

class Notification(models.Model):
    TYPES = [('DUE_SOON', 'Due Soon'), ('CHANGE', 'Project Change')]
    
    # Unique related_name: app_notifications
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='app_notifications') 
    message = models.CharField(max_length=255)
    is_read = models.BooleanField(default=False)
    notification_type = models.CharField(max_length=20, choices=TYPES)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']