from django.shortcuts import render
from incidents.models import Service, ActivityLog, Incidents, Team, OnCallSchedule
from django.utils.timezone import now
import json
from django.views.decorators.csrf import csrf_exempt
from incidents.response import response_wrapper
from incidents.utils import notify_on_call_users, check_api_status


@csrf_exempt
def report_incidents(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        title = data.get('title')
        description = data.get('description')
        team_id = data.get('team_id')
        urgency = data.get('urgency')
        resolved = data.get('resolved')
        status = data.get('status')
        
        team = Team.objects.get(id=team_id)
        incident = Incidents.objects.create(
            title=title,
            description=description,
            team=team,
            urgency=urgency,
            resolved=resolved,
            status=status,
        )
        
        notify_on_call_users(team, incident)
        
        return response_wrapper(incident, status_code=201, message="Incident Reported")
    return response_wrapper({}, status_code=400, message="Error: Invalid request method")
        
    
@csrf_exempt
def report_activity_logs(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        error_message = data.get('error_message')
        stack_trace = data.get('stack_trace')
        error, created = ActivityLog.objects.get_or_create(
            error_message=error_message,
            stack_trace=stack_trace,
            defaults={
                'created_at': now(),
            }
        )
        if not created:
            error.occurence_count += 1
            error.updated_at = now()
            error.save()
        
        return response_wrapper(error, status_code=201, message="Activity Log Reported")
    return response_wrapper({}, status_code=400, message="Error: Invalid request method")


@csrf_exempt
def report_host(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        host = data.get('host')
        description = data.get('description')
        
        service, created = Service.objects.get_or_create(
            host=host,
            defaults={
                'description': description,
                'created_at': now(),
            }
        )
        if not created:
            service.description = description
            service.save()
        
        return response_wrapper(service, status_code=201, message="Host Added")
    return response_wrapper({}, status_code=400, message="Error: Invalid request method")


def dashboard(request):
    activity_logs = ActivityLog.objects.all().order_by('-updated_at')
    schedules = OnCallSchedule.objects.all().order_by('-start_time' )
    services = Service.objects.all()
    hosts = {service.id: service.host for service in services}
    
    statuses = check_api_status(hosts)
    return render(request, 'dashboard.html', {'services': services, 'activity_logs': activity_logs,
                                              'schedules': schedules, 'statuses': statuses})
