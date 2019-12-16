from django.shortcuts import reverse

from api import EventAPI
from panel.component.CustomElements import Choices
from panel.module.base.block.CustomPages import AbstractBasePage
from panel.module.base.block.CustomComponents import BlockObject
from panel.module.base.block.CustomComponents import BlockSet
from panel.module.base.block.CustomComponents import PageObject


class EventPage(AbstractBasePage):
    def generateList(self):
        event_type = dict((y, x) for x, y in Choices().getEventTypeChoices())[self.param["type"]]

        def genDict(status):
            events = event_api.filterSelf(event_status=status, event_type=event_type)
            event_dict = map(lambda event: dict(
                element_text=event.event_name,
                element_link=reverse(
                    'panel.module.management_event.view_dispatch_param',
                    args=['activity', event.id]),
                elements=[
                    dict(
                        text='Teams',
                        link=reverse(
                            'panel.module.management_event.view_dispatch_param',
                            args=['team', event.id]
                        )
                    ),
                    dict(
                        text='Races (WIP)',
                        link='#'
                    ),
                    dict(
                        text='Manage',
                        link=event_api.getEventModifyLink(self.param["type"], id=event.id)
                    )
                ]
            ),
                             [event for event in events])
            return BlockObject(status, 'Event', ['', '', ''], event_dict)

        event_api = EventAPI(self.request)
        return BlockSet().makeBlockSet(genDict('future'), genDict('running'), genDict('done'))

    def render(self):
        header = dict(
            button=dict(
                link=reverse(
                    'panel.module.management_data.view_dispatch_param',
                    args=[self.param["type"], 'custom']
                )+'?action=add&base=event_mgmt',
                text='Add Event'
            )
        )
        return super().renderHelper(PageObject('Events List', self.generateList(), header))

    def parseParams(self, param):
        super().parseMatch('(\w+\s\w+)')
        param = dict(type=param)
        return param
