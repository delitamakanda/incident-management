from django.contrib.auth import get_user_model
from ninja import Schema
from ninja.orm import create_schema
from typing import List, Dict

UsernameSchemaMixin = create_schema(
    get_user_model(),
    fields=[get_user_model().USERNAME_FIELD],
)

EmailSchemaMixin = create_schema(
    get_user_model(),
    fields=[get_user_model().EMAIL_FIELD],
)

UserLogout = create_schema(
    get_user_model(),
    exclude=['password'],
)


class LoginIn(UsernameSchemaMixin):
    password: str


class RequestPasswordReset(EmailSchemaMixin):
    pass


class SetPasswordIn(UsernameSchemaMixin):
    new_password: str
    new_password_confirm: str
    token: str
    

class ChangePasswordIn(Schema):
    old_password: str
    new_password: str
    new_password_confirm: str
    

class ErrorOutput(Schema):
    error: Dict[str, List[str]]

