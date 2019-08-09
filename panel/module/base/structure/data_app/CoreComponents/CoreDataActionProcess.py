from abc import abstractmethod

from misc.CustomFunctions import LogFunctions
from misc.CustomElements import Dispatcher
from panel.module.base.structure.data_app.constants import ActionType
from panel.module.base.structure.data_app.CoreComponents.CoreDataComponentConstructor import CoreDataComponentConstructor


class CoreDataActionProcess(CoreDataComponentConstructor):
    def __init__(self, request, app_name, base_class, mutable, guard):
        super().__init__(request, app_name, base_class, mutable, guard)
        self.process_dispatcher = self.__setProcessDispatcher()

    def __setProcessDispatcher(self):
        dispatcher = Dispatcher()
        dispatcher.add(ActionType.ADD, self._add)
        dispatcher.add(ActionType.EDIT, self._edit)
        dispatcher.add(ActionType.DELETE, self._delete)
        return dispatcher

    # View Process Functions
    def process(self, action, **kwargs):
        self.process_dispatcher.get(action)(**kwargs)
        LogFunctions.generateLog(
            request=self.request, 
            log_type=AuthenticationMetaAPI(self.request).getAuthType(), 
            message='Core Data App Process - App: {}, Action: {}, Base Class: {}'.format(
                self.app_name, self.action, self.base_class
            )
        )

    @abstractmethod
    def _add(self, **kwargs):
        pass

    @abstractmethod
    def _edit(self, **kwargs):
        pass

    @abstractmethod
    def _delete(self, **kwargs):
        pass
