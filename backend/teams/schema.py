from ninja import ModelSchema
from teams.models import Team

class TeamSchema(ModelSchema):
    class Config:
        model = Team
        model_fields = ['id', 'first_name', 'last_name', 'email', 'phone_number', 'avatar', 'oncall', 'shift_start', 'shift_end']
