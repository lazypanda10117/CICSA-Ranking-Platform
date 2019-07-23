from django.shortcuts import render

from api.authentication import AuthenticationGuard
from api.authentication import AuthenticationGuardType


def index(request):
    AuthenticationGuard(AuthenticationGuardType.LOGIN_GUARD, request).guard()
    return render(request, 'platform/index.html')
