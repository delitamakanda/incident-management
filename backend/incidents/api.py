from ninja import Router
from ninja.pagination import paginate
from .models import Incidents
from teams.models import Team
from typing import List
from django.shortcuts import get_object_or_404
from .schema import IncidentsSchema
from django.contrib.auth.models import User
from incidentmanagement.pagination import CustomPagination

router = Router()

@router.get('', response=List[IncidentsSchema])
@paginate(CustomPagination)
def get_incidents(request):
    qs = Incidents.objects.all()
    return qs

@router.get('/{team_id}/list', response=List[IncidentsSchema])
@paginate(CustomPagination)
def get_incidents_by_assigned(request, team_id: str):
    team_obj = Team.objects.get(id=team_id)
    qs = Incidents.objects.filter(assigned_to=team_obj.created_by)
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
