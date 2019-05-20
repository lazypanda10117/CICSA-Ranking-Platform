from attrdict import AttrDict
from abc import ABC
from misc.CustomFunctions import RequestFunctions
from api.authentication.AuthenticationFactory import AuthenticationFactory
from api.authentication_api.AuthenticationMetaAPI import AuthenticationMetaAPI


class AbstractAPI(ABC):
    def __init__(self, request):
        self.request = request
        utype = self.request.session['utype'] if RequestFunctions.sessionChecker(self.request, 'utype') else None
        self.auth = AuthenticationFactory(utype).dispatch()
        self.auth_meta = AuthenticationMetaAPI(self.request)
        self.context = AttrDict(
            authID=self.auth_meta.getAuthenticatedID(),
            authType=self.auth_meta.getAuthType()
        )