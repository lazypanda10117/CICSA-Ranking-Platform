from abc import abstractmethod
from misc.CustomFunctions import ModelFunctions, AuthFunctions
from ..base.AbstractAPI import AbstractAPI


class GeneralModelAPI(AbstractAPI):
    def __init__(self, request):
        super().__init__(request)
        self.base = self.setBaseClass()
        self.class_name = self.base.__class__.__name__
        self.auth_class = self.auth(request).dispatch(self.class_name)

    @abstractmethod
    def setBaseClass(self):
        pass;

    def verifySelf(self, **kwargs):
        result = ModelFunctions.getModelObject(self.base, **kwargs)
        result = self.auth_class(self.request).authenticate('edit', result)
        AuthFunctions.raise404Empty(result)
        return result

    def getSelf(self, **kwargs):
        result = ModelFunctions.getModelObject(self.base, **kwargs)
        return self.auth_class(self.request).authenticate('view', result)

    def filterSelf(self, **kwargs):
        result = ModelFunctions.filterModelObject(self.base, **kwargs)
        return self.auth_class(self.request).authenticate('view', result)
