from abc import ABC
from misc.CustomFunctions import RequestFunctions
from ..authentication.AuthenticationFactory import AuthenticationFactory


class AbstractAPI(ABC):
    def __init__(self, request):
        self.request = request
        utype = self.request.session['utype'] if RequestFunctions.sessionChecker(self.request, 'utype') else None
        self.auth = AuthenticationFactory(utype).dispatch()
