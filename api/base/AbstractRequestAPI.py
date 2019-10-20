from abc import ABC
from misc.CustomFunctions import RequestFunctions
from api.authentication.AuthenticationFactory import AuthenticationFactory


# This is the only unguarded Core Fundamental API
# because the information it retrieves is public information
class AbstractRequestAPI(ABC):
    def __init__(self, request):
        self.request = request
        utype = RequestFunctions.sessionGetter(request, 'utype')
        self.auth = AuthenticationFactory(utype).dispatch()
