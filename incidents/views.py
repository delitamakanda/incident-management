from django.shortcuts import render
from incidents.models import Service, ActivityLog, Incidents, Team, OnCallSchedule, Token, DESCRIPTION_CHOICES, \
    STATUS_CHOICES, URGENCY_CHOICES
from django.utils.timezone import now
import json
from django.views.decorators.csrf import csrf_exempt
from incidents.response import response_wrapper
from incidents.utils import notify_on_call_users, check_api_status
from django.contrib.auth import authenticate, get_user_model
from incidents.decorators import token_required

user_model = get_user_model()

@csrf_exempt
def authenticate_user(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')
        
        user = authenticate(username=username, password=password)
        
        if user is not None:
            token, _ = Token.objects.get_or_create(user=user)
            return response_wrapper({
                'token': token.key,
                'user_id':user.id,
                'username': user.username,
            }, status_code=200, message="User authenticated successfully")
        else:
            return response_wrapper({}, status_code=401, message="Invalid username or password")
    return response_wrapper({}, status_code=400, message="Error: Invalid request method")


@csrf_exempt
def verify_token(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        token = data.get('token')
        
        try:
            token_obj = Token.objects.get(key=token)
            return response_wrapper({
                'user_id': token_obj.user.id,
                'username': token_obj.user.username,
            }, status_code=200, message="Token verified successfully")
        except Token.DoesNotExist:
            return response_wrapper({}, status_code=401, message="Invalid token")
    return response_wrapper({}, status_code=400, message="Error: Invalid request method")


@token_required
@csrf_exempt
def logout_user(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        token = data.get('token')
        
        try:
            token_obj = Token.objects.get(key=token)
            token_obj.delete()
            return response_wrapper({}, status_code=200, message="User logged out successfully")
        except Token.DoesNotExist:
            return response_wrapper({}, status_code=401, message="Invalid token")
    return response_wrapper({}, status_code=400, message="Error: Invalid request method")


@token_required
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


@token_required
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


@csrf_exempt
def dashboard(request):
    activity_logs = ActivityLog.objects.all().order_by('-updated_at')
    schedules = OnCallSchedule.objects.all().order_by('-start_time' )
    services = Service.objects.all()
    hosts = {service.id: service.host for service in services}
    
    statuses = check_api_status(hosts)
    return render(request, 'dashboard.html', {'services': services, 'activity_logs': activity_logs,
                                              'schedules': schedules, 'statuses': statuses})

@token_required
@csrf_exempt
def list_urgency_levels(request):
    if request.method == 'GET':
        urgency_levels = URGENCY_CHOICES
        return response_wrapper(urgency_levels, status_code=200)
    return response_wrapper({}, status_code=400, message="Error: Invalid request method")

@token_required
@csrf_exempt
def list_status_levels(request):
    if request.method == 'GET':
        return response_wrapper(STATUS_CHOICES, status_code=200)
    return response_wrapper({}, status_code=400, message="Error: Invalid request method")

@token_required
@csrf_exempt
def list_descriptions(request):
    if request.method == 'GET':
        return response_wrapper(DESCRIPTION_CHOICES, status_code=200)
    return response_wrapper({}, status_code=400, message="Error: Invalid request method")
