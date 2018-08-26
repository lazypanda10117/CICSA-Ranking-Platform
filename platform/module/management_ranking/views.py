from django.views.decorators.csrf import csrf_exempt

from blackbox.block_app.base.Base import *
from .CustomPages import EventPage, EventActivityPage, EventActivityRankingPage
from .CustomProcesses import UpdateEventStatusProcess, EventActivityRankingProcess


def index(request):
    return ManagementRankingView().home(request);


def viewDispatch(request, route, param=''):
    dispatcher = ManagementRankingView().setViewDispatcher();
    object = dispatcher.get(route)(request, param);
    return object.render();


@csrf_exempt
def processDispatch(self, request, dispatch_path, param=''):
    dispatcher = self.setProcessDispatcher();
    object = dispatcher.get(dispatch_path)(request, param);
    return object.process();


class ManagementRankingView(AbstractBlockApp.AppView):
    ### Block App Base View Interited Functions
    def home(self, request):
        return super().index(request, 'blackbox.block_app.management_ranking.view_dispatch', ['event']);

    def setViewDispatcher(self):
        dispatcher = Dispatcher();
        dispatcher.add('event', EventPage);
        dispatcher.add('activity', EventActivityPage);
        dispatcher.add('activity ranking', EventActivityRankingPage);
        return dispatcher;

    def setProcessDispatcher(self):
        dispatcher = Dispatcher();
        dispatcher.add('activity status', UpdateEventStatusProcess);
        dispatcher.add('activity ranking', EventActivityRankingProcess);
        return dispatcher;