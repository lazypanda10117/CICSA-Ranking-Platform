from ..base.AbstractAPI import AbstractAPI


class AuthenticationMetaAPI(AbstractAPI):
    def getAuthType(self):
        return self.auth(self.request).getAuthenticationType()
