from api.authentication import AuthenticationType


class AuthenticationPublic:
    @staticmethod
    def getIdentifier():
        return AuthenticationType.PUBLIC

    @staticmethod
    def getAllowedModules():
        allowedModules = []
        return allowedModules
