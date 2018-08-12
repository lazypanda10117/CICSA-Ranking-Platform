from django.shortcuts import reverse
from blackbox import api, CustomElements
from blackbox.block_app.base.CustomPages import AbstractBasePage
from blackbox.block_app.base.CustomComponents import BlockObject, BlockSet, PageObject



class EventDisplay(AbstractBasePage):
    def generateList(self):
        event_type = dict((y, x) for x, y in CustomElements.Choices().getEventTypeChoices())[self.param];
        def genDict(status):
            events = event_api.getEvents(event_status=status, event_type=event_type);
            event_dict = map(lambda event: dict(
                element_text=event.event_name,
                element_link=reverse(
                    'blackbox.block_app.management_event.view_dispatch',
                    args=['activity', event.id]),
                elements=[
                    dict(
                        text='Modify',
                        link=event_api.getEventModifyLink(self.param, id=event.id)
                    )
                ]
            ),
                             [event for event in events]);
            return BlockObject(status, 'Event', ['Modify'], event_dict);

        event_api = api.EventAPI(self.request);
        return BlockSet().makeBlockSet(genDict('future'), genDict('running'), genDict('Done'));

    def render(self):
        header = dict(
            button=dict(
                link=reverse('adminCustomView', args=[self.param])+'?action=add',
                text='Add Event'
            )
        );
        return super().renderHelper(PageObject('Events List', self.generateList(), header))