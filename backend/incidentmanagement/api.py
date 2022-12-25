from ninja import NinjaAPI
from incidents.api import router as incidents_router
from teams.api import router as teams_router

api = NinjaAPI()

api.add_router('/incidents/', incidents_router, tags=['incidents'])
api.add_router('/teams/', teams_router, tags=['teams'])
