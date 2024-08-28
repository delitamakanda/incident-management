from ninja import Router
from ninja.pagination import paginate
from .models import Incidents, ActivityLog, Notification, Service,  Host
from typing import List
from django.shortcuts import get_object_or_404
from .schema import IncidentsSchema, ActivityLogSchema, NotificationSchema, HostSchema, ServiceSchema
from django.contrib.auth.models import User
from incidentmanagement.pagination import CustomPagination

router = Router()


@router.get('', response=List[IncidentsSchema])
@paginate(CustomPagination)
def get_incidents(request):
    qs = Incidents.objects.all()
    return qs


@router.get('/{user_id}/list/', response=List[IncidentsSchema])
@paginate(CustomPagination)
def get_incidents_by_assigned(request, user_id: int):
    qs = Incidents.objects.filter(assigned_to=user_id)
    return qs


@router.get('/{incident_id}', response=IncidentsSchema)
def get_incident(request, incident_id: str):
    qs = get_object_or_404(Incidents, id=incident_id)
    return qs


@router.post('/create/')
def create_incident(request, payload: IncidentsSchema):
    user_id = User.objects.get(id=payload.assigned_to)
    payload.assigned_to = user_id
    incident = Incidents.objects.create(**payload.dict())
    return {"id": incident.id}


@router.put('/{incident_id}')
def update_incident(request, incident_id: str, payload: IncidentsSchema):
    incident = get_object_or_404(Incidents, id=incident_id)
    for attr, value in payload.dict().items():
        setattr(incident, attr, value)
    incident.save()
    return {"success": True}


@router.delete('/{incident_id}')
def delete_incident(request, incident_id: str):
    incident = get_object_or_404(Incidents, id=incident_id)
    incident.delete()
    return {"success": True}


@router.get('logs', response=List[ActivityLogSchema])
@paginate(CustomPagination)
def get_activity_logs(request):
    qs = ActivityLog.objects.all()
    return qs


@router.get('notifications', response=List[NotificationSchema])
@paginate(CustomPagination)
def get_notifications(request):
    qs = Notification.objects.all()
    return qs


@router.put('notifications/{notification_id}')
def update_notifications(request, notification_id: str, payload: NotificationSchema):
    notification = get_object_or_404(Notification, id=notification_id)
    for attr, value in payload.dict().items():
        setattr(notification, attr, value)
    notification.save()
    return {"success": True}


@router.get('hosts', response=List[HostSchema])
@paginate(CustomPagination)
def get_hosts(request):
    qs = Host.objects.all()
    return qs


@router.get('services', response=List[ServiceSchema])
@paginate(CustomPagination)
def get_services(request):
    qs = Service.objects.all()
    return qs
