from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Service, ActivityLog
from django.core.mail import send_mail
from django.contrib.auth import get_user_model
from django.conf import settings

User = get_user_model()


@receiver(post_save, sender=Service)
def send_notification(sender, instance, **kwargs):
    if instance.status == 'critical':
        send_mail(
            'Critical Service Alert',
            f'Critical service {instance.name} has been detected.',
            settings.EMAIL_HOST_USER,
            [settings.ADMIN_EMAIL],
            fail_silently=False,
        )


@receiver(post_save, sender=Service)
def log_activity(sender, instance, created, **kwargs):
    if created:
        send_mail(
            'New Error Log',
            f'Error: {instance.error_message}\nStack Trace:\n{instance.stack_trace}',
            settings.DEFAULT_FROM_EMAIL,
            [settings.ADMIN_EMAIL],
            fail_silently=False,
        )