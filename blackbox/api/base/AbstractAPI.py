from abc import ABC, abstractmethod
from blackbox.auth_app.AuthenticationFactory import AuthenticaitonFactory


# not much use of a class right now, but might be more useful later
class AbstractAPI():
    def __init__(self, request):
        self.request = request;
        self.auth = AuthenticaitonFactory(self.request.session['utype']).dispatch();

