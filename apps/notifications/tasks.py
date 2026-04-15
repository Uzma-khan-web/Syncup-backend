from celery import shared_task
from django.utils import timezone
from datetime import timedelta
from django.core.mail import send_mail
from apps.tasks.models import Task  # Aapka existing task model
from .models import Notification

@shared_task
def send_deadline_reminders():
    # Kal ki date calculate karein
    tomorrow = timezone.now().date() + timedelta(days=1)
    upcoming_tasks = Task.objects.filter(due_date=tomorrow, status='TODO')

    for task in upcoming_tasks:
        # 1. In-App Notification create karein
        Notification.objects.create(
            user=task.user,
            message=f"Kal deadline hai: {task.title}",
            notification_type='DUE_SOON'
        )

        # 2. Email bhejein
        send_mail(
            subject="SyncUp: Task Due Tomorrow!",
            message=f"Hi {task.user.username}, aapka task '{task.title}' kal khatam hone wala hai.",
            from_email="noreply@syncup.com",
            recipient_list=[task.user.email],
        )