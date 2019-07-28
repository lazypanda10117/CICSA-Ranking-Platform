from abc import abstractmethod

from misc.CustomElements import Dispatcher
from panel.component.CustomElements import Form
from panel.module.base.structure.data_app.CoreComponents.CoreDataComponentConstructor import \
    CoreDataComponentConstructor
from panel.module.base.structure.data_app.constants import ActionType
from panel.module.base.structure.data_app.utils import QueryTermUtils


class CoreDataFormView(CoreDataComponentConstructor):
    def __init__(self, request, app_name, base_class, mutable=False):
        super().__init__(request, app_name, base_class, mutable)
        self.validation_set = self._setValidationSet()
        self.populate_data_dispatcher = self.__setPopulateDataDispatcher()

    @abstractmethod
    def _setValidationSet(self):
        pass

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

    def render(self, **kwargs):
        app_name = kwargs.pop('app_name')
        action = kwargs.pop('action')
        route = kwargs.pop('route')

        data = dict(
            field_data=self.getFieldData(**kwargs),
            choice_data=self.getChoiceData(**kwargs),
            multi_choice_data=self.getMultiChoiceData(**kwargs)
        )

        special_context = dict(
            search=self.getSearchElement(**kwargs)
        )

        return Form(
            form_path='_{}_form'.format(action),
            form_name=route,
            form_action=action,
            destination=QueryTermUtils(self.request).getRedirectDestination(app_name=app_name, route=route),
            data=data,
            special_context=special_context
        )
