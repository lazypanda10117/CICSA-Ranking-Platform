from abc import abstractmethod

from misc.CustomElements import Dispatcher
from panel.module.base.structure.data_app.CoreComponents.CoreDataComponentConstructor import \
    CoreDataComponentConstructor
from panel.module.base.structure.data_app.constants import ActionType
from panel.module.base.structure.data_app.constants import ComponentType


class CoreDataPage(CoreDataComponentConstructor):
    def __init__(self, request, app_name, base_class, mutable=False):
        super().__init__(request, app_name, base_class, mutable)
        self.action_permission_dispatcher = self._setActionPermissionDispatcher()
        self.associated_component_class_dispatcher = self._setAssociatedComponentClassDispatcher()

    @abstractmethod
    def _setAssociatedComponentClassDispatcher(self):
        dispatcher = Dispatcher()
        dispatcher.add(ComponentType.TABLE, None)
        dispatcher.add(ComponentType.FORM, None)
        dispatcher.add(ComponentType.PROCESS, None)
        return dispatcher

    def _setActionPermissionDispatcher(self):
        dispatcher = Dispatcher()
        dispatcher.add(ActionType.VIEW, True)
        dispatcher.add(ActionType.ADD, True)
        dispatcher.add(ActionType.EDIT, self.mutable)
        dispatcher.add(ActionType.DELETE, self.mutable)
        return dispatcher

    def generateData(self, **kwargs):
        action = kwargs.pop('action')
        route = kwargs.pop('route')
        element_id = kwargs.pop('element_id')

        if action == ActionType.VIEW:
            return self.associated_component_class_dispatcher.get(ComponentType.TABLE).render(route=route)

        if action == ActionType.ADD:
            return self.associated_component_class_dispatcher.get(ComponentType.FORM).render(action=action)

        if action in [ActionType.EDIT, ActionType.DELETE] and element_id is not None:
            return self.associated_component_class_dispatcher.get(ComponentType.FORM).render(
                action=action, element_id=element_id
            )

        raise Exception("Unmatched parameters core data generation")

    def processData(self, **kwargs):
        action = kwargs.pop("action")
        element_id = kwargs.pop('element_id')
        self.associated_component_class_dispatcher.get(ComponentType.PROCESS).process(
            action=action,
            element_id=element_id
        )
