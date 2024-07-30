from ninja import NinjaAPI, Swagger
from incidents.api import router as incidents_router
from incidents.auth.api import router as auth_router
from teams.api import router as teams_router
from workspaces.api import router as workspaces_router

api = NinjaAPI(docs=Swagger())

api.add_router('/incidents/', incidents_router, tags=['incidents'])
api.add_router('/teams/', teams_router, tags=['teams'])
api.add_router('/workspaces/', workspaces_router, tags=['workspaces'])
api.add_router('/auth/', auth_router, tags=['auth'])


@api.get("/", response=dict)
def check_health(request):  # Health check endpoint
    return {"status_code": 200, "message": "API is running"}
