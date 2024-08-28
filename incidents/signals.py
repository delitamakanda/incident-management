from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Service
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
            ['admin@localhost'],
            fail_silently=False,
        )
