from abc import ABC
from abc import abstractmethod

from misc.CustomElements import Dispatcher
from panel.module.base.structure.data_app.constants import ActionType


class CoreDataActionProcess(ABC):
    def __init__(self):
        self.process_dispatcher = self.__setProcessDispatcher()

    def __setProcessDispatcher(self):
        dispatcher = Dispatcher()
        dispatcher.add(ActionType.ADD, self.add)
        dispatcher.add(ActionType.EDIT, self.edit)
        dispatcher.add(ActionType.DELETE, self.delete)
        return dispatcher

    # View Process Functions
    def process(self, action, **kwargs):
        self.process_dispatcher.get(action)(**kwargs)

    @abstractmethod
    def add(self, **kwargs):
        pass

    @abstractmethod
    def edit(self, **kwargs):
        pass

    @abstractmethod
    def delete(self, **kwargs):
        pass
