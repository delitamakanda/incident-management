import uuid
import os
import binascii
from datetime import datetime, timedelta

from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.contrib.auth.models import User


class DateTimeStamp(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        abstract = True
        ordering = ['-id']
        
        
class Token(models.Model):
    key = models.CharField(max_length=40, primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='auth_token')
    created_at = models.DateTimeField(auto_now_add=True)
    expiry_date = models.DateTimeField(null=True)
    
    def save(self, *args, **kwargs):
        if not self.key:
            self.key = binascii.hexlify(os.urandom(20)).decode()
        if not self.expiry_date or self.expiry_date < datetime.now():
            self.expiry_date = datetime.now() + timedelta(days=7)  # Set expiry date to 7 days from now
        super().save(*args, **kwargs)
        
    def __str__(self):
        return self.key


class Team(DateTimeStamp):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    members = models.ManyToManyField(User, related_name='teams')
    
    class Meta:
        verbose_name = 'Team'
        verbose_name_plural = 'Teams'
        ordering = ['id']
        unique_together = ('name',)
    
    def __str__(self):
        return self.name
    
    def get_members(self):
        return ', '.join([member.username for member in self.members.all()])
    
    def get_member_count(self):
        return self.members.count()
    
    def get_open_incident_count(self):
        return self.incidents.filter(status__lt=2).count()
    
    def get_resolved_incident_count(self):
        return self.incidents.filter(status__gt=0).count()
    
    def get_closed_incident_count(self):
        return self.incidents.filter(status=2).count()
    
    def get_total_incident_count(self):
        return self.incidents.count()
    
    def get_average_resolution_time(self):
        total_resolution_time = sum([incident.resolution_time for incident in self.incidents.filter(status__gt=0)])
        average_resolution_time = total_resolution_time / self.get_resolved_incident_count() if self.get_resolved_incident_count() > 0 else 0
        return average_resolution_time
    
    def get_average_response_time(self):
        total_response_time = sum([incident.response_time for incident in self.incidents.filter(status__lt=2)])
        average_response_time = total_response_time / self.get_open_incident_count() if self.get_open_incident_count() > 0 else 0
        return average_response_time
    
    def get_average_impact_score(self):
        total_impact_score = sum([incident.impact_score for incident in self.incidents.filter(status__lt=2)])
        average_impact_score = total_impact_score / self.get_open_incident_count() if self.get_open_incident_count() > 0 else 0
        return average_impact_score
    

class OnCallSchedule(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    
    class Meta:
        verbose_name = 'On Call Schedule'
        verbose_name_plural = 'On Call Schedules'
        ordering = ['start_time']
        unique_together = ('team', 'user','start_time', 'end_time')
    
    def __str__(self):
        return f'{self.user.username} on-call {self.team.name}'
    
    def get_duration(self):
        return (self.end_time - self.start_time).total_seconds() / 60
    
    def get_status(self):
        if self.start_time <= datetime.now() <= self.end_time:
            return 'On-call'
        elif self.start_time > datetime.now():
            return 'Upcoming'
        else:
            return 'Off-call'


STATUS_CHOICES = (
    (0, 'OK'),
    (1, 'WARNING'),
    (2, 'CRITICAL'),
    (3, 'UNKNOWN'),
    (4, 'DOWN'),
    (5, 'UNREACHABLE'),
)

LOW = 'LOW'
HIGH = 'HIGH'
NORMAL = 'NORMAL'
URGENCY_CHOICES = (
    (LOW, 'Low'),
    (HIGH, 'High'),
    (NORMAL, 'Normal'),
)
DEVOPS_ESCALATION = 'DevOps Escalation'
SECURITY_ESCALATION = 'Security Ops Escalation'
PERFORMANCE_ESCALATION = 'Performance Ops Escalation'
BREAKDOWN_ESCALATION = 'Breakdown Ops Escalation'
DESCRIPTION_CHOICES = (
    (DEVOPS_ESCALATION, 'Devops Escalation'),
    (SECURITY_ESCALATION, 'Security Ops Escalation'),
    (PERFORMANCE_ESCALATION, 'Performance Ops Escalation'),
    (BREAKDOWN_ESCALATION, 'Breakdown Ops Escalation'),
)


class Incidents(DateTimeStamp):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    urgency = models.CharField(max_length=255, choices=URGENCY_CHOICES, default=NORMAL)
    resolved = models.BooleanField(default=False)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default=0)
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=255, choices=DESCRIPTION_CHOICES, default=DEVOPS_ESCALATION)
    reported_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "%s" % self.title

    class Meta:
        verbose_name = "Incident"
        verbose_name_plural = "Incidents"
        ordering = ['id']
        unique_together = ('team', 'id')
        
    def get_status_display(self):
        return dict(STATUS_CHOICES)[self.status]
    
    def get_description_display(self):
        return dict(DESCRIPTION_CHOICES)[self.description]
    
    def get_urgency_display(self):
        return dict(URGENCY_CHOICES)[self.urgency]


class Escalation(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    level = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1), MaxValueValidator(8)])
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    class Meta:
        verbose_name = "Escalation"
        verbose_name_plural = "Escalations"
        ordering = ['level']
        unique_together = ('team', 'level', 'user')
    
    def __str__(self):
        return f"Level {self.level} escalation for {self.team.name} by {self.user.username}"


class ActivityLog(DateTimeStamp):
    error_message = models.TextField()
    stack_trace = models.TextField()
    occurence_count = models.PositiveIntegerField(default=1)
    resolved = models.BooleanField(default=False)

    def __str__(self):
        return f"Error Log: {self.error_message}"

    class Meta:
        verbose_name = "Activity Log"
        verbose_name_plural = "Activity Logs"
        ordering = ['-id']


class Service(DateTimeStamp):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    host = models.URLField(max_length=1000)
    description = models.TextField(blank=True)
    
    def __str__(self):
        return f"Service: {self.host}"
    
    class Meta:
        verbose_name = "Service"
        verbose_name_plural = "Services"
        ordering = ['id']
        unique_together = ('host',)
    
        

    
    



