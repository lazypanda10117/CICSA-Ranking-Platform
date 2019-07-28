from misc.CustomElements import Dispatcher
from panel.module.ModuleRegistry import ModuleRegistry
from panel.module.base.structure.data_app.CoreViews import CoreDataView
from panel.module.management_event.CustomComponents import sth

class EventDataPage(CoreDataView):
    def _setAppName(self):
        return ModuleRegistry.MANAGEMENT_EVENT

    def _setViewDispatcher(self):
        dispatcher = Dispatcher()
        dispatcher.add('')
        return dispatcher

    def _getTemplateBase(self):
        pass

