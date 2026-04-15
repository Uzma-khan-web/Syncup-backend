from celery import shared_task
from django.utils import timezone
from datetime import timedelta
from django.core.mail import send_mail
from .models import Task, Notification

@shared_task
def send_deadline_reminders():
    tomorrow = timezone.now().date() + timedelta(days=1)
    upcoming_tasks = Task.items.filter(due_date=tomorrow, status='TODO')

    for task in upcoming_tasks:
        # 1. Create In-App Notification
        Notification.objects.create(
            user=task.user,
            message=f"Reminder: Task '{task.title}' is due tomorrow!",
            notification_type='DUE_SOON'
        )

        # 2. Send Email
        send_mail(
            subject="Task Due Tomorrow!",
            message=f"Hi {task.user.username}, your task '{task.title}' is reaching its deadline on {task.due_date}.",
            from_email="noreply@syncup.com",
            recipient_list=[task.user.email],
        )