from .AbstractDisplayClass import *

from admin_console.generalFunctions import *
from admin_console.HelperClass import *
from admin_console.API import *


class EventDisplay(AbstractDisplayClass):
    def generateList(self):
        event_type = dict((y, x) for x, y in Choices().getEventTypeChoices())[self.param];
        def genDict(status):
            events = event_api.getEvents(event_status=status, event_type=event_type);
            event_dict = map(lambda event: dict(
                element_text=event.event_name,
                element_link=reverse('eventManagementDispatch', args=['activity', event.id]),
                elements=[
                    dict(
                        text='Modify',
                        link=event_api.getEventModifyLink(id=event.id)
                    )
                ]
            ),
                             [event for event in events]);
            return dict(block_title=status, element_name='Event', header=['Modify'], contents=event_dict);

        event_api = EventAPI(self.request);
        return dict(future=genDict('future'), running=genDict('running'), done=genDict('done'));

    def render(self):
        return kickRequest(self.request, True, render(
            self.request, 'event_management/eventDisplayList.html',
            {'title': 'Events List', 'element_list': self.generateList(),
             'header': {'button': {'link': reverse('adminCustomView', args=[self.param])+'?action=add',
                                   'text': 'Add Event'}}}));
