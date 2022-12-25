from ninja import Router
from .models import Incidents
from typing import List
from django.shortcuts import get_object_or_404
from .schema import IncidentsSchema

router = Router()

@router.get('', response=List[IncidentsSchema])
def get_incidents(request):
    qs = Incidents.objects.all()
    return qs

@router.get('/{incident_id}', response=IncidentsSchema)
def get_incident(request, incident_id: int):
    qs = get_object_or_404(Incidents, id=incident_id)
    return qs

@router.post('/create')
def create_incident(request, payload: IncidentsSchema):
    incident = Incidents.objects.create(**payload.dict())
    return {"id": incident.id}

@router.put('/{incident_id}')
def update_incident(request, incident_id: int, payload: IncidentsSchema):
    incident = get_object_or_404(Incidents, id=incident_id)
    for attr, value in payload.items():
        setattr(incident, attr, value)
    incident.save()
    return {"success": True}

@router.delete('/{incident_id}')
def delete_incident(request, incident_id: int):
    incident = get_object_or_404(Incidents, id=incident_id)
    incident.delete()
    return {"success": True}
