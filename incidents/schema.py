from ninja import ModelSchema
from incidents.models import Incidents, ActivityLog, Notification, Service, Host

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
        
        
class ServiceSchema(ModelSchema):
    class Config:
        model = Service
        model_fields = ['id', 'name', 'check_command',
                        'check_interval', 'last_check', 'status', 'last_output',]
        
        
class HostSchema(ModelSchema):
    class Config:
        model = Host
        model_fields = ['id', 'name', 'ip_address', 'description',
                        'created_at', 'updated_at',]
        
        