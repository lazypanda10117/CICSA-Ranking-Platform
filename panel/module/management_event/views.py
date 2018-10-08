from django.views.decorators.csrf import csrf_exempt
from misc.CustomElements import Dispatcher
from ..base.block.Base import AbstractBlockApp
from .CustomPages import EventPage, EventActivityPage, EventActivityDetailPage, EventChoicePage
from .CustomProcesses import EventChoiceProcess


def index(request):
    return ManagementEventView().home()


def viewDispatch(request, route, param=''):
    return ManagementEventView().viewDispatch(request, route, param)


@csrf_exempt
def processDispatch(request, route, param=''):
    return ManagementEventView().processDispatch(request, route, param)


class ManagementEventView(AbstractBlockApp.AppView):
    # Block App Base View Inherited Functions

    def home(self):
        return super().index('panel.module.management_event.view_dispatch', ['choice'])

    def setViewDispatcher(self):
        dispatcher = Dispatcher()
        dispatcher.add('choice', EventChoicePage)
        dispatcher.add('event', EventPage)
        dispatcher.add('activity', EventActivityPage)
        dispatcher.add('activity detail', EventActivityDetailPage)
        return dispatcher

    def setProcessDispatcher(self):
        dispatcher = Dispatcher()
        dispatcher.add('choice', EventChoiceProcess)
        return dispatcher