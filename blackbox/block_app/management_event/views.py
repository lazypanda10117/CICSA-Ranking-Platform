from blackbox.block_app.base.Base import *
from .CustomPages import EventPage, EventActivityPage, EventActivityDetailPage, EventChoicePage
from .CustomProcesses import EventChoiceProcess

class ManagementEventView(AbstractBlockApp.AppView):
    ### Block App Base View Interited Functions

    def home(self, request):
        return super().index(request, 'blackbox.block_app.management_event.view_dispatch', ['choice']);

    def setViewDispatcher(self):
        dispatcher = Dispatcher();
        dispatcher.add('choice', EventChoicePage);
        dispatcher.add('event', EventPage);
        dispatcher.add('activity', EventActivityPage);
        dispatcher.add('activity detail', EventActivityDetailPage);
        return dispatcher;

    def setProcessDispatcher(self):
        dispatcher = Dispatcher();
        dispatcher.add('choice', EventChoiceProcess);
        return dispatcher;