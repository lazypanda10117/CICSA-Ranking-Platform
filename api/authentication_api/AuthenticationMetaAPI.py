from api.base import AbstractRequestAPI
from misc.CustomFunctions import RequestFunctions


class AuthenticationMetaAPI(AbstractRequestAPI):
    def getAuthType(self):
        return self.auth(self.request).getAuthenticationType()

    def getAuthenticatedID(self):
        return RequestFunctions.sessionGetter(self.request, 'uid')
