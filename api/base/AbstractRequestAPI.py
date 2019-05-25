from abc import ABC
from misc.CustomFunctions import RequestFunctions
from api.authentication.AuthenticationFactory import AuthenticationFactory


class AbstractRequestAPI(ABC):
    def __init__(self, request):
        self.request = request
        utype = RequestFunctions.sessionGetter(request, 'utype')
        self.auth = AuthenticationFactory(utype).dispatch()
