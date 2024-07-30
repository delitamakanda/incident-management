from ninja import Router
from .models import Team
from typing import List
from .schema import TeamSchema
from django.shortcuts import get_object_or_404

router = Router()

@router.get("/", response=List[TeamSchema])
def get_teams(request):
    qs = Team.objects.all()
    return qs

@router.get("/{team_id}", response=TeamSchema)
def get_team(request, team_id: str):
    qs = get_object_or_404(Team, id=team_id)
    return qs

@router.post("/create/")
def create_team(request, payload: TeamSchema):
    team = Team.objects.create(**payload.dict())
    return {"id": team.id }

@router.put("/{team_id}")
def update_team(request, team_id: str, payload: TeamSchema):
    team = get_object_or_404(Team, id=team_id)
    for attr, value in payload.dict().items():
        setattr(team, attr, value)
    team.save()
    return {"success": True }

@router.delete("/{team_id}")
def delete_team(request, team_id: str):
    team = get_object_or_404(Team, id=team_id)
    team.delete()
    return {"success": True}
