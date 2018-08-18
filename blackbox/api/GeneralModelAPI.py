from abc import ABC
from .AbstractAPI import AbstractAPI
from misc.GeneralFunctions import generalFunctions as gf


class GeneralModelAPI(AbstractAPI, ABC):
    def __init__(self, request):
        super().__init__(request);
        self.funcBindingSetup();

    def funcBindingSetup(self):
        class_name = self.base.__class__.__name__;
        setattr(self, 'get' + class_name, self.getFuncBinder(class_name));
        setattr(self, 'filter' + class_name, self.filterFuncBinder(class_name));

    def getFuncBinder(self, class_name):
        def getModelVal(**kwargs):
            return gf.getModelObject(self.base, **kwargs);
        getModelVal.__name__ = 'get'+class_name;
        return getModelVal;

    def filterFuncBinder(self, class_name):
        def filterModelVal(**kwargs):
            return gf.filterModelObject(self.base, **kwargs);
        filterModelVal.__name__ = 'filter'+class_name;
        return filterModelVal;
