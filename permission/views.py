from django.shortcuts import render

from misc.CustomElements import Dispatcher
from api.authentication import AuthenticationGuard
from api.authentication import AuthenticationGuardType
from permission.CustomClasses.Login import Login


def dispatch(request, route):
    return PermissionView().setFunctionDispatcher().get(route)(request)


class PermissionView:
    def __init__(self):
        self.permission_object = Login

    def setFunctionDispatcher(self):
        dispatcher = Dispatcher()
        dispatcher.add('login', self.login)
        dispatcher.add('logout', self.logout)
        dispatcher.add('view', self.view)
        return dispatcher

    def login(self, request):
        return self.permission_object(request).login()

    def logout(self, request):
        return self.permission_object(request).logout()

    @staticmethod
    def view(request):
        return AuthenticationGuard(AuthenticationGuardType.PUBLIC_GUARD, request).guard(
            api=False, rend=render(request, 'permission/login.html')
        )
