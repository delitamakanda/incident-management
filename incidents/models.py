import uuid
from django.db import models
from django.contrib.auth.models import User


STATUT_CHOICES = (
    (0, 'In progress'),
    (1, 'Resolved'),
    (2, 'Closed'),
    (3, 'Pending'),
    (4, 'Investigating'),
    (5, 'Remediated'),
    (6, 'Out of Scope'),
    (7, 'Deferred'),
    (8, 'Canceled'),
    (9, 'Reopened'),
)

STATUS_CHOICES = (
    (0, 'OK'),
    (1, 'WARNING'),
    (2, 'CRITICAL'),
    (3, 'UNKNOWN'),
    (4, 'DOWN'),
    (5, 'UNREACHABLE'),
)


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
        
        
class Host(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    ip_address = models.GenericIPAddressField()
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Host"
        verbose_name_plural = "Hosts"
        ordering = ['id']


class Service(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    host = models.ForeignKey(Host, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    check_command = models.CharField(max_length=255)
    check_interval = models.PositiveIntegerField()
    last_check = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default=0)
    last_output = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return "%s (%s)" % (self.host.name, self.name)
    
    class Meta:
        verbose_name = "Service"
        verbose_name_plural = "Services"
        ordering = ['id']
        

    
    



