from django.contrib import admin
from teams.models import Team

class TeamAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'phone_number', 'oncall')
    list_filter = ('oncall',)
    search_fields = ('first_name','last_name', 'phone_number')

admin.site.register(Team, TeamAdmin)