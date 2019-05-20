from abc import abstractmethod
from api.base.AbstractAPI import AbstractAPI
from misc.CustomFunctions import AuthFunctions
from misc.CustomFunctions import LogFunctions
from misc.CustomFunctions import ModelFunctions


class GeneralModelAPI(AbstractAPI):
    def __init__(self, request):
        super().__init__(request)
        self.base = self.getBaseClass()
        self.class_name = self.base.__class__.__name__
        self.auth_class = self.auth(request).dispatch(self.class_name)

    @staticmethod
    @abstractmethod
    def getBaseClass():
        pass

    def verifySelf(self, **kwargs):
        result = ModelFunctions.getModelObject(self.base, **kwargs)
        result = self.auth_class(self.request).authenticate('edit', result)
        AuthFunctions.raise404Empty(result)
        LogFunctions.generateLog(self.request, self.context.authType,
                                 LogFunctions.makeLogQueryFromObject(self.class_name, 'edit', result))
        return result

    def addSelf(self, obj):
        if isinstance(obj, self.base):
            result = self.auth_class(self.request).authenticate('add', obj)
            AuthFunctions.raise404Empty(result)
            LogFunctions.generateLog(self.request, self.context.authType,
                                     LogFunctions.makeLogQueryFromObject(self.class_name, 'add', result))
            return result
        else:
            AuthFunctions.raise404Empty()

    def deleteSelf(self, **kwargs):
        result = ModelFunctions.getModelObject(self.base, **kwargs)
        result = self.auth_class(self.request).authenticate('delete', result)
        AuthFunctions.raise404Empty(result)
        LogFunctions.generateLog(self.request, self.context.authType,
                                 LogFunctions.makeLogQueryFromObject(self.class_name, 'delete', result))
        return result

    def getSelf(self, **kwargs):
        result = ModelFunctions.getModelObject(self.base, **kwargs)
        return self.auth_class(self.request).authenticate('view', result)

    def filterSelf(self, **kwargs):
        result = ModelFunctions.filterModelObject(self.base, **kwargs)
        return self.auth_class(self.request).authenticate('view', result)

    def excludeSelf(self, **kwargs):
        result = ModelFunctions.excludeModelObject(self.base, **kwargs)
        return self.auth_class(self.request).authenticate('view', result)

    def getAll(self):
        result = ModelFunctions.filterModelObject(self.base)
        return self.auth_class(self.request).authenticate('view', result)
