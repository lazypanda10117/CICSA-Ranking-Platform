from abc import ABC
from misc.GeneralFunctions import generalFunctions as gf
from blackbox.api.base.AbstractAPI import AbstractAPI

class GeneralModelAPI(AbstractAPI, ABC):
    def __init__(self, request):
        super().__init__(request);
        self.class_name = self.base.__class__.__name__;
        self.__funcBindingSetup();

    def __funcBindingSetup(self):
        setattr(self, 'get' + self.class_name, self._getFuncBinder());
        setattr(self, 'filter' + self.class_name, self._filterFuncBinder());

    def _getFuncBinder(self):
        def _getModelVal(**kwargs):
            return self.auth(self.request).dispatch(self.class_name).authenticate([gf.getModelObject(self.base, **kwargs)]);
        _getModelVal.__name__ = 'get' + self.class_name;
        return _getModelVal;

    def _filterFuncBinder(self):
        def _filterModelVal(**kwargs):
            return self.auth(self.request).dispatch(self.class_name).authenticate(gf.filterModelObject(self.base, **kwargs));
        _filterModelVal.__name__ = 'filter' + self.class_name;
        return _filterModelVal;
