from celery import shared_task
from celery.utils.log import get_task_logger
from django.core.mail import send_mail
from django.contrib.auth import get_user_model
from .models import Service
import subprocess
from django.conf import settings

logger = get_task_logger(__name__)
User = get_user_model()


@shared_task
def check_services():
    for service in Service.objects.all():
        try:
            subprocess.check_output(service.check_command, shell=True, stderr=subprocess.STDOUT)
            logger.info(f"Service {service.name} is running.")
        except subprocess.CalledProcessError as e:
            logger.error(f"Service {service.name} is down. Error: {e.output.decode('utf-8')}")
            # Send notification to admins
            admins = User.objects.filter(is_superuser=True)
            for admin in admins:
                send_mail(
                    'Service Status Update',
                    f'Service {service.name} is down. Error: {e.output.decode("utf-8")}',
                    settings.DEFAULT_FROM_EMAIL,
                    [admin.email],
                    fail_silently=False,
                )
        
@shared_task
def check_service(service_id):
    service = Service.objects.get(id=service_id)
    result = subprocess.run(service.check_command, shell=True, capture_output=True, text=True)
    service.last_output = result.stdout
    service.status = "OK" if result.returncode == 0 else "CRITICAL"
    service.save()
    logger.info(f"Service {service.name} status updated. Result: {service.status}")
