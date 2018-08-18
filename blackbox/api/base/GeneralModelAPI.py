from abc import ABC
from blackbox.api.base.AbstractAPI import AbstractAPI
from misc.GeneralFunctions import generalFunctions as gf


class GeneralModelAPI(AbstractAPI, ABC):
    def __init__(self, request):
        super().__init__(request);
        self.__funcBindingSetup();

    def __funcBindingSetup(self):
        class_name = self.base.__class__.__name__;
        setattr(self, 'get' + class_name, self._getFuncBinder(class_name));
        setattr(self, 'filter' + class_name, self._filterFuncBinder(class_name));

    def _getFuncBinder(self, class_name):
        def _getModelVal(**kwargs):
            return gf.getModelObject(self.base, **kwargs);
        _getModelVal.__name__ = 'get'+class_name;
        return _getModelVal;

    def _filterFuncBinder(self, class_name):
        def _filterModelVal(**kwargs):
            return gf.filterModelObject(self.base, **kwargs);
        _filterModelVal.__name__ = 'filter'+class_name;
        return _filterModelVal;
