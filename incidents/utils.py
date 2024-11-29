import requests
import logging

from django.core.mail import send_mail
from incidents.models import OnCallSchedule, Escalation, Incidents
from django.conf import settings
from django.utils.timezone import now

logger = logging.getLogger(__name__)

def notify_on_call_users(team, incident):
    current_time = now()
    on_call_schedules = OnCallSchedule.objects.filter(
        team=team,
        start_time__lte=current_time,
        end_time__gte=current_time
    )
    
    for schedule in on_call_schedules:
        send_mail(
            f"Incident Reported : {incident.title}",
            f'A new incident has been reported: {incident.description}.\nPlease review and take appropriate action.',
            settings.DEFAULT_FROM_EMAIL,
            [schedule.user.email],
            fail_silently=False,
        )
        
def escalate_incident(incident):
    escalations = Escalation.objects.filter(
        team=incident.team,
    ).order_by('level')
    
    for escalation in escalations:
        notify_on_call_users(incident.team, incident)
        
        logger.info(f"Escalating incident {incident.title} to level {escalation.level}")
        

def check_api_status(hosts):
    statuses = {}
    for name, url in hosts.items():
        try:
            response = requests.get(url,timout=5)
            statuses[name] = {
                "status_code": response.status_code,
                "status": "OK" if response.status_code == 200 else "Failed",
            }
        except requests.exceptions.RequestException as e:
            logger.error(f"Error checking API status for {name}: {e}")
            statuses[name] = {
                "status_code": -1,
                "status": "Failed",
            }
    return statuses
            