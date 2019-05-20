from api.base.AbstractAPI import AbstractAPI
from misc.CustomFunctions import RequestFunctions


class AuthenticationMetaAPI(AbstractAPI):
    def getAuthType(self):
        return self.auth(self.request).getAuthenticationType()

    def getAuthenticatedID(self):
        return RequestFunctions.sessionGetter(self.request, 'uid')
