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
    DESCRIPTION_CHOICES = (
        (DEVOPS_ESCALATION, 'Devops Escalation'),
        (SECURITY_ESCALATION, 'Security Ops Escalation'),
    )
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    urgency = models.CharField(max_length=255, choices=URGENCY_CHOICES, default=NORMAL)
    triggered = models.BooleanField(default=False)
    acknowledged = models.BooleanField(default=False)
    resolved = models.BooleanField(default=False)
    description = models.CharField(max_length=255, choices=DESCRIPTION_CHOICES, default=DEVOPS_ESCALATION)
    assigned_to = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.assigned_to.username if self.assigned_to else None

    class Meta:
        verbose_name = "Incident"
        verbose_name_plural = "Incidents"
        ordering = ['id']
