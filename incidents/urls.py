from django.urls import path
from incidents.views import (dashboard, report_activity_logs, report_incidents, report_host, authenticate_user, logout_user, verify_token,
                             list_descriptions, list_status_levels, list_urgency_levels)

urlpatterns = [
    path('', dashboard, name='dashboard'),
    path('api/report-activity-logs/', report_activity_logs, name='report_activity_logs'),
    path('api/report-incidents/', report_incidents, name='report_incidents'),
    path('api/report-host/', report_host, name='report_host'),
    path('api/authenticate/', authenticate_user, name='authenticate_user'),
    path('api/logout/', logout_user, name='logout_user'),
    path('api/verify-token/', verify_token, name='verify_token'),
    path('api/list-descriptions/', list_descriptions, name='list_descriptions'),
    path('api/list-status-levels/', list_status_levels, name='list_status_levels'),
    path('api/list-urgency-levels/', list_urgency_levels, name='list_urgency_levels'),
]
