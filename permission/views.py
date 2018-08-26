from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from misc.Dispatcher import Dispatcher
from misc.GeneralFunctions import generalFunctions as gf
from .Login import Login


@csrf_exempt
def dispatch(request, route):
    return PermissionView().setFunctionDispatcher().get(route)(request);


class PermissionView():
    def __init__(self):
        self.permission_object = Login;

    def setFunctionDispatcher(self):
        dispatcher = Dispatcher();
        dispatcher.add('login', self.login);
        dispatcher.add('logout', self.logout);
        dispatcher.add('view', self.view);
        return dispatcher;

    def login(self, request):
        return self.permission_object(request).login();

    def logout(self, request):
        return self.permission_object(request).logout();

    def view(self, request):
        return gf.kickRequest(request, False, render(request, 'blackbox/platform/login/login.html'));
