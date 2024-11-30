# incident-management  application
incident management cms with django

[![incident management CI](https://github.com/delitamakanda/incident-management/actions/workflows/django.yml/badge.svg?event=push)](https://github.com/delitamakanda/incident-management/actions/workflows/django.yml)

## Notes:
- User: Leveraging Django's built-in user model for authentication.
- Service: Services can be nested.
- ActivityLog: Tracks actions performed by users for auditing and history purposes.
- Incidents: Represents bugs submitted by users
- Team: Reprends Team On-Call
- OnCallSchedule: Represents Schedule On-Call
- Escalation: Represents Escalation Policies


## API DOCS
Access the API Documentation: Navigate to http://127.0.0.1:8000/api/ to view the automatically generated Swagger documentation.

method POST
```curl
api/report-activity-logs/
```
```curl
api/report-incidents/
```

```curl
api/report-host/
```

get a token to access content
```curl
api/authenticate/
```

```curl
api/logout/
```
```curl
api/verify-token/
```

method GET
```curl
api/list-descriptions/
```

```curl
api/list-status-levels/
```

```curl
api/list-urgency-levels/
```