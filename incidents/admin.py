from django.contrib import admin
from incidents.models import Incidents


class IncidentsAdmin(admin.ModelAdmin):
    list_display = ('urgency', 'description','triggered','created_at')
    list_filter = ('urgency','triggered')
    search_fields = ('id', 'description','urgency','triggered')


admin.site.register(Incidents, IncidentsAdmin)
