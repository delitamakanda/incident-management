from ninja import ModelSchema
from incidents.models import Incidents

class IncidentsSchema(ModelSchema):
    class Config:
        model = Incidents
        model_fields = ['id', 'urgency', 'triggered', 'acknowledged', 'resolved', 'description', 'assigned_to', 'created_at', 'updated_at']

