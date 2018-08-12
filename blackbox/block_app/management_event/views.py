from blackbox.block_app.base.Base import *
from .CustomPages import EventDisplay, EventActivityPage, EventActivityDetailPage


class ManagementEventView(AbstractBlockApp.AppView):
    ### Block App Base View Interited Functions

    def home(self, request):
        return super().index(request, 'blackbox.block_app.management_event.choice');

    def setViewDispatcher(self):
        dispatcher = Dispatcher();
        dispatcher.add('event', EventDisplay);
        dispatcher.add('activity', EventActivityPage);
        dispatcher.add('activity detail', EventActivityDetailPage);
        return dispatcher;

    ### Management Event View Specific Functions

    def choice(self, request):
        types = [value.event_type_name for value in gf.filterModelObject(EventType)];
        type_style = {'width': int(12 / len(types)) if len(types) else None}
        return gf.kickRequest(request, True,
                              render(request, 'console/event.html', {'types': types, 'type_style': type_style}));

    def eventFilter(self, request, type):
        return redirect(reverse('blackbox.block_app.management_event.view_dispatch', args=['event', type]));