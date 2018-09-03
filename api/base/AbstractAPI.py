from abc import ABC
from ..authentication.AuthenticationFactory import AuthenticationFactory


# not much use of a class right now, but might be more useful later
class AbstractAPI(ABC):
    def __init__(self, request):
        self.request = request
        self.auth = AuthenticationFactory(self.request.session['utype']).dispatch()
