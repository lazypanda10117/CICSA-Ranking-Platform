from abc import ABC
from abc import abstractmethod

from misc.CustomElements import Dispatcher
from panel.module.base.structure.data_app.CoreComponents.CoreDataComponentConstructor import \
    CoreDataComponentConstructor
from panel.module.base.structure.data_app.constants import ActionType


class CoreDataFormView(CoreDataComponentConstructor):
    def __init__(self, request, base_class, mutable=False):
        super().__init__(request, base_class, mutable)
        self.populate_data_dispatcher = self.__setPopulateDataDispatcher()

    @abstractmethod
    def getFieldData(self, **kwargs):
        pass

    def __setPopulateDataDispatcher(self):
        dispatcher = Dispatcher()
        dispatcher.add(ActionType.ADD, False)
        dispatcher.add(ActionType.EDIT, True)
        dispatcher.add(ActionType.DELETE, True)
        return dispatcher

    # Default return values for custom form components
    def getChoiceData(self, **kwargs):
        return None

    def getDBMap(self, **kwargs):
        return None

    def getMultiChoiceData(self, **kwargs):
        return None

    def getSearchElement(self, **kwargs):
        return None

    def generateFormData(self, **kwargs):
        data = dict(
            field_data=self.getFieldData(**kwargs),
            choice_data=self.getChoiceData(**kwargs),
            multi_choice_data=self.getMultiChoiceData(**kwargs)
        )
        special_field = dict(
            search=self.getSearchElement(**kwargs)
        )
        return dict(data=data, special_field=special_field)
