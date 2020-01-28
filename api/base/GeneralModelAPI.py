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
        self.class_name = self.base.__name__
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
        LogFunctions.generateLog(
            self.request,
            self.context.authType,
            "{} {} with kwargs {}".format("CREATE", self.class_name, kwargs)
        )
        obj.save()

    # Prev Conf: might need to change name to editSelf
    def verifySelf(self, legacy=True, **kwargs):
        if legacy:
            result = ModelFunctions.getModelObject(self.base, **kwargs)
        else:
            result = ModelFunctions.filterModelObject(self.base, **kwargs)
        result = self.auth_class(self.request).authenticate(AuthenticationActionType.EDIT, result)
        LogFunctions.generateLog(
            self.request,
            self.context.authType,
            "{} {} with kwargs {}".format("VERIFY", self.class_name, kwargs)
        )
        return result

    def addSelf(self, obj):
        if isinstance(obj, self.base):
            result = self.auth_class(self.request).authenticate(AuthenticationActionType.ADD, obj)
            AuthFunctions.raise404Empty(result)
            LogFunctions.generateLog(
                self.request,
                self.context.authType,
                "{} {} with kwargs {}".format("ADD", self.class_name, obj.__dict__)
            )
            return result
        else:
            AuthFunctions.raise404Empty()

    def deleteSelf(self, legacy=True, **kwargs):
        if legacy:
            result = ModelFunctions.getModelObject(self.base, **kwargs)
        else:
            result = ModelFunctions.filterModelObject(self.base, **kwargs)
        result = self.auth_class(self.request).authenticate(AuthenticationActionType.DELETE, result)
        LogFunctions.generateLog(
            self.request,
            self.context.authType,
            "{} {} with kwargs {}".format("DELETE", self.class_name, kwargs)
        )
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
