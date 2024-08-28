from __future__ import absolute_import, unicode_literals

from celery import Celery
from celery.app import shared_task
from celery.schedules import crontab
from incidents.models import Service
from incidents.tasks import check_service
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'incidentmanagement.settings')

app = Celery('incidentmanagement')

app.config_from_object('django.conf:settings', namespace='CELERY')


@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    # Call every 5 minutes
    sender.add_periodic_task(crontab(minute='*/5'), check_all_services.s(),)
    

@shared_task
def check_all_services():
    from incidents.tasks import check_services
    check_services()
    print("Services checked")
    for service in Service.objects.all():
        print(f"Service {service.name} is {service.status}")
        check_service.delay(service.id)


app.autodiscover_tasks()
