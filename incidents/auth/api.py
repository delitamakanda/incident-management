from ninja import Router
from django.conf import settings
from ninja.security import django_auth
from django.contrib.auth import get_user_model, update_session_auth_hash
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.forms import (PasswordResetForm, SetPasswordForm, PasswordChangeForm)
from django.contrib.auth import (
    authenticate, login, logout
)

from .schema import (
    LoginIn, RequestPasswordReset, SetPasswordIn, ChangePasswordIn, ErrorOutput, UserLogout
)

router = Router()


@router.post("/login/", response={200: UserLogout, 403: ErrorOutput}, auth=None)
def login_view(request, data: LoginIn):
    user = authenticate(backend="django.contrib.auth.backends.ModelBackend", **data.dict())
    if user is not None and user.is_active:
        login(request, user, backend="django.contrib.auth.backends.ModelBackend")
        return user
    return 403, None


@router.post("/logout/", response={200: UserLogout}, auth=django_auth)
def logout_view(request):
    logout(request)
    return {"message": "Logged out successfully"}


@router.post("/password/reset/", response={200: UserLogout}, auth=None)
def password_reset_view(request, data: RequestPasswordReset):
    form = PasswordResetForm(data=data.dict())
    if form.is_valid():
        form.save(
            request=request,
            extra_email_context=(
                {
                    "domain": settings.DOMAIN,
                    "site_name": settings.SITE_NAME,
                    "protocol": "https" if settings.SECURE_SSL_REDIRECT else "http",
                    "token_generator": default_token_generator,
                    "uid": form.cleaned_data["uid"],
                    "token": form.cleaned_data["token"],
                    "request": request,
                }
            )
        )
    return 200, None


@router.post("/me/", response={200: UserLogout}, auth=django_auth)
def me(request):
    return request.user


@router.post("/password/reset/confirm/", response={200: UserLogout}, auth=None)
def password_reset_confirm_view(request, data: SetPasswordIn):
    user_field = get_user_model().USERNAME_FIELD
    user_data = {user_field: getattr(data, user_field)}
    user = get_user_model().objects.filter(**user_data)
    if user.exists():
        user = user.first()
        if default_token_generator.check_token(user, data.token):
            form = SetPasswordForm(user, data=data.dict())
            if form.is_valid():
                form.save()
                login(request, user, backend="django.contrib.auth.backends.ModelBackend")
                return user
            return 400, {"errors": dict(form.errors)}
        return 400, {"errors": {"token": ["Invalid token."]}}
    
    
@router.post("/password/change/", response={200: UserLogout, 403: ErrorOutput}, auth=django_auth)
def password_change_view(request, data: ChangePasswordIn):
    form = PasswordChangeForm(request.user, data=data.dict())
    if form.is_valid():
        update_session_auth_hash(request, form.save())
        return 200
    return 400, {"errors": dict(form.errors)}
        
        
    