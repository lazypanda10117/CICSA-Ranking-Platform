from blackbox import api
from blackbox.block_app.base.Base import *
from .CustomPages import EventPage, EventActivityPage, EventActivityRankingPage
from .CustomProcesses import UpdateEventStatusProcess, EventActivityRankingProcess

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