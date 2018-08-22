from abc import ABC, abstractmethod
from misc.GeneralFunctions import generalFunctions as gf
from blackbox.api.base.AbstractAPI import AbstractAPI


class GeneralModelAPI(AbstractAPI, ABC):
    def __init__(self, request):
        super().__init__(request);
        self.base = self.setBaseClass();
        self.class_name = self.base.__class__.__name__;
        self.auth_class = self.auth(request).dispatch(self.class_name);
        self.__funcBindingSetup();

    @abstractmethod
    def setBaseClass(self):
        pass;

    def __funcBindingSetup(self):
        setattr(self, 'get' + self.class_name, self._getFuncBinder());
        setattr(self, 'filter' + self.class_name, self._filterFuncBinder());

    def _getFuncBinder(self):
        def _getModelVal(**kwargs):
            result = [gf.getModelObject(self.base, **kwargs)];
            return self.auth_class.authenticate('view', result);
        _getModelVal.__name__ = 'get' + self.class_name;
        return _getModelVal;

    def _filterFuncBinder(self):
        def _filterModelVal(**kwargs):
            result = gf.filterModelObject(self.base, **kwargs);
            return self.auth_class.authenticate('view', result);
        _filterModelVal.__name__ = 'filter' + self.class_name;
        return _filterModelVal;