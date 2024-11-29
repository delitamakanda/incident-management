from django.urls import path
from incidents.views import dashboard, report_activity_logs, report_incidents, report_host

urlpatterns = [
    path('', dashboard, name='dashboard'),
    path('api/report-activity-logs/', report_activity_logs, name='report_activity_logs'),
    path('api/report-incidents/', report_incidents, name='report_incidents'),
    path('api/report-host/', report_host, name='report_host'),
]
