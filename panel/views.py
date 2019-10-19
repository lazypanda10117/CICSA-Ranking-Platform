from django.shortcuts import render

from api.authentication import AuthenticationGuard
from api.authentication import AuthenticationGuardType


def index(request):
    return AuthenticationGuard(AuthenticationGuardType.LOGIN_GUARD, request).guard(
            api=False, rend=render(request, 'platform/index.html')
        )
