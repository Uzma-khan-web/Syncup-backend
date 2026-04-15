from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Task
from apps.notifications.models import Notification

@receiver(post_save, sender=Task)
def task_change_alert(sender, instance, created, **kwargs):
    if not created: # Sirf update hone par trigger hoga
        Notification.objects.create(
            user=instance.user,
            message=f"Project Update: '{instance.title}' mein changes kiye gaye hain.",
            notification_type='CHANGE'
        )