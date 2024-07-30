from ninja import ModelSchema
from incidents.models import Incidents, ActivityLog, Notification

class IncidentsSchema(ModelSchema):
    class Config:
        model = Incidents
        model_fields = ['id', 'urgency', 'triggered', 'acknowledged', 'resolved', 'description', 'assigned_to', 'created_at', 'updated_at', 'statut', 'notes']


class ActivityLogSchema(ModelSchema):
    class Config:
        model = ActivityLog
        model_fields = ['id', 'incident', 'created_at', 'updated_at']


class NotificationSchema(ModelSchema):
    class Config:
        model = Notification
        model_fields = ['id', 'incident', 'created_at', 'updated_at', 'sms', 'email', 'call']