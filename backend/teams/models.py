import uuid
from django.db import models
from django.contrib.auth.models import User
from incidents.models import Incidents

class Team(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255, unique=True)
    phone_number = models.CharField(max_length=20)
    avatar = models.CharField(max_length=255, blank=True, null=True)
    oncall = models.BooleanField(default=False)
    shift_start = models.DateTimeField(blank=True, null=True)
    shift_end = models.DateTimeField(blank=True, null=True)
    incidents = models.ManyToManyField(Incidents, blank=True)
    created_by = models.ForeignKey(User, related_name='teams', on_delete=models.CASCADE)

    def __str__(self):
        return "%s %s" % (self.first_name, self.last_name)

    class Meta:
        verbose_name = "Team Member"
        verbose_name_plural = "Team Members"
        ordering = ['id']
