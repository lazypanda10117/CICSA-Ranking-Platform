from abc import ABC
from misc.CustomFunctions import MiscFunctions, RequestFunctions
from ..authentication.AuthenticationFactory import AuthenticationFactory


# not much use of a class right now, but might be more useful later
class AbstractAPI(ABC):
    def __init__(self, request):
        self.request = request
        utype = self.request.session['utype'] if RequestFunctions.sessionChecker(self.request, ['utype']) else None
        self.auth = AuthenticationFactory(utype).dispatch()
