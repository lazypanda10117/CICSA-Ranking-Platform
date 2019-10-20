from django.views.decorators.csrf import csrf_exempt

from misc.CustomElements import Dispatcher
from panel.module.ModuleRegistry import ModuleRegistry
from panel.module.base.block.Base import AbstractBlockApp
from panel.module.management_event.CustomPages import EventPage
from panel.module.management_event.CustomPages import EventActivityPage
from panel.module.management_event.CustomPages import EventActivityDetailPage
from panel.module.management_event.CustomPages import EventChoicePage
from panel.module.management_event.CustomPages import EventTeamPage
from panel.module.management_event.CustomProcesses import UpdateParticipatingTeamsProcess


def index(request):
    return ManagementEventView().home(request)


def viewDispatch(request, route, param=''):
    return ManagementEventView().viewDispatch(request, route, param)


@csrf_exempt
def processDispatch(request, route, param=''):
    return ManagementEventView().processDispatch(request, route, param)


class ManagementEventView(AbstractBlockApp.AppView):
    # Block App Base View Inherited Functions
    def getBaseAppName(self):
        return ModuleRegistry.MANAGEMENT_EVENT

    def home(self, request):
        return super().index(request, 'panel.module.management_event.view_dispatch', ['choice'])

    def setViewDispatcher(self):
        dispatcher = Dispatcher()
        dispatcher.add('choice', EventChoicePage)
        dispatcher.add('event', EventPage)
        dispatcher.add('activity', EventActivityPage)
        dispatcher.add('activity detail', EventActivityDetailPage)
        dispatcher.add('team', EventTeamPage)
        return dispatcher

    def setProcessDispatcher(self):
        dispatcher = Dispatcher()
        dispatcher.add('update teams', UpdateParticipatingTeamsProcess)
        return dispatcher
