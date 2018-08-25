from abc import ABC, abstractmethod
from misc.GeneralFunctions import generalFunctions as gf
from blackbox.api.base.AbstractAPI import AbstractAPI


class GeneralModelAPI(AbstractAPI, ABC):
    def __init__(self, request):
        super().__init__(request);
        self.base = self.setBaseClass();
        self.class_name = self.base.__class__.__name__;
        self.auth_class = self.auth(request).dispatch(self.class_name);

    @abstractmethod
    def setBaseClass(self):
        pass;

    def getSelf(self, **kwargs):
        result = gf.getModelObject(self.base, **kwargs);
        return self.auth_class(self.request).authenticate('view', result);

    def filterSelf(self, **kwargs):
        result = gf.filterModelObject(self.base, **kwargs);
        return self.auth_class(self.request).authenticate('view', result);