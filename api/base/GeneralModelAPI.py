from abc import abstractmethod

from api.authentication import AuthenticationActionType
from api.base import AbstractCoreAPI
from misc.CustomFunctions import AuthFunctions
from misc.CustomFunctions import LogFunctions
from misc.CustomFunctions import ModelFunctions


class GeneralModelAPI(AbstractCoreAPI):
    def __init__(self, request):
        super().__init__(request)
        self.base = self.getBaseClass()
        self.class_name = self.base.__class__.__name__
        self.auth_class = self.auth(request).dispatch(self.class_name)

    @staticmethod
    @abstractmethod
    def getBaseClass():
        pass

    # Can only create one object, different from addSelf, which verifies if the object is addable
    def createSelf(self, **kwargs):
        obj = self.base()
        for key, val in kwargs.items():
            setattr(obj, key, val)
        result = self.auth_class(self.request).authenticate(AuthenticationActionType.ADD, obj)
        AuthFunctions.raise404Empty(result)
        LogFunctions.generateLog(self.request, self.context.authType,
                                 LogFunctions.makeLogQueryFromObject(self.base, AuthenticationActionType.ADD, result))
        obj.save()

    def verifySelf(self, **kwargs):
        result = ModelFunctions.getModelObject(self.base, **kwargs)
        result = self.auth_class(self.request).authenticate(AuthenticationActionType.EDIT, result)
        AuthFunctions.raise404Empty(result)
        LogFunctions.generateLog(self.request, self.context.authType,
                                 LogFunctions.makeLogQueryFromObject(self.base, AuthenticationActionType.EDIT, result))
        return result

    def addSelf(self, obj):
        if isinstance(obj, self.base):
            result = self.auth_class(self.request).authenticate(AuthenticationActionType.ADD, obj)
            AuthFunctions.raise404Empty(result)
            LogFunctions.generateLog(self.request, self.context.authType,
                                     LogFunctions.makeLogQueryFromObject(self.base, AuthenticationActionType.ADD, result))
            return result
        else:
            AuthFunctions.raise404Empty()

    def deleteSelf(self, **kwargs):
        result = ModelFunctions.getModelObject(self.base, **kwargs)
        result = self.auth_class(self.request).authenticate(AuthenticationActionType.DELETE, result)
        AuthFunctions.raise404Empty(result)
        LogFunctions.generateLog(self.request, self.context.authType,
                                 LogFunctions.makeLogQueryFromObject(self.base, AuthenticationActionType.DELETE, result))
        return result

    def getSelf(self, **kwargs):
        result = ModelFunctions.getModelObject(self.base, **kwargs)
        return self.auth_class(self.request).authenticate(AuthenticationActionType.VIEW, result)

    def filterSelf(self, **kwargs):
        result = ModelFunctions.filterModelObject(self.base, **kwargs)
        return self.auth_class(self.request).authenticate(AuthenticationActionType.VIEW, result)

    def excludeSelf(self, **kwargs):
        result = ModelFunctions.excludeModelObject(self.base, **kwargs)
        return self.auth_class(self.request).authenticate(AuthenticationActionType.VIEW, result)

    def getAll(self):
        result = ModelFunctions.filterModelObject(self.base)
        return self.auth_class(self.request).authenticate(AuthenticationActionType.VIEW, result)
