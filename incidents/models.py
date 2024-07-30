import uuid
from django.db import models
from django.contrib.auth.models import User

class Incidents(models.Model):
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
    STATUT_CHOICES = (
        (0, 'In progress'),
        (1, 'Resolved'),
        (2, 'Closed'),
    )
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    urgency = models.CharField(max_length=255, choices=URGENCY_CHOICES, default=NORMAL)
    triggered = models.BooleanField(default=False)
    acknowledged = models.BooleanField(default=False)
    resolved = models.BooleanField(default=False)
    statut = models.CharField(max_length=1, choices=STATUT_CHOICES, default=0)
    description = models.CharField(max_length=255, choices=DESCRIPTION_CHOICES, default=DEVOPS_ESCALATION)
    notes = models.TextField(blank=True, null=True)
    assigned_to = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "%s (%s)" % (self.urgency, self.id)

    class Meta:
        verbose_name = "Incident"
        verbose_name_plural = "Incidents"
        ordering = ['id']


class ActivityLog(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    incident = models.ForeignKey(Incidents, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "%s (%s)" % (self.incident, self.id)

    class Meta:
        verbose_name = "Activity Log"
        verbose_name_plural = "Activity Logs"
        ordering = ['-id']

class Notification(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    incident = models.OneToOneField(Incidents, on_delete=models.CASCADE)
    sms = models.BooleanField(default=False)
    email = models.BooleanField(default=False)
    call = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "%s (%s)" % (self.incident, self.id)
    
    class Meta:
        verbose_name = "Notification"
        verbose_name_plural = "Notifications"
        ordering = ['-id']



