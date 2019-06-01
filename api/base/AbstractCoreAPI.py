from attrdict import AttrDict
from api.base import AbstractRequestAPI
from api.authentication_api import AuthenticationMetaAPI


class AbstractCoreAPI(AbstractRequestAPI):
    def __init__(self, request):
        super().__init__(request)
        self.request = request
        self.context = self.__setContext()

    def __setContext(self):
        auth_meta = AuthenticationMetaAPI(self.request)
        return AttrDict(
            authID=auth_meta.getAuthenticatedID(),
            authType=auth_meta.getAuthType()
        )
