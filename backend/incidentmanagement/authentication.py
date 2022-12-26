import jwt
from ninja.security import HttpBearer
from django.conf import settings

class GlobalAuhentication(HttpBearer):
    def authenticate(self, request, token):
        try:
            JWT_SIGNING_KEY = getattr(settings, 'JWT_SIGNING_KEY', None)
            payload = jwt.decode(token, JWT_SIGNING_KEY, algorithms=['HS256'])
            username: str = payload.get('sub')
            if username is None:
                return None
        except jwt.PyJWTError:
            return None

        return username
