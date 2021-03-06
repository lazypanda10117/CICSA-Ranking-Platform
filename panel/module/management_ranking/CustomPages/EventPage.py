from django.shortcuts import reverse
from api import EventAPI
from ...base.block.CustomPages import AbstractBasePage
from ...base.block.CustomComponents import BlockObject, BlockSet, PageObject


class EventPage(AbstractBasePage):
    def generateList(self):
        def genDict(status):
            events = event_api.filterSelf(event_status=status)
            change_status_dict = dict(future='running', running='done', done='not applicable')
            event_dict = list(map(lambda event: dict(
                element_text=event.event_name,
                element_link=reverse(
                    'panel.module.management_ranking.view_dispatch_param',
                    args=['activity', event.id]),
                elements=[
                    dict(
                        text=change_status_dict[event.event_status],
                        link=reverse(
                            'panel.module.management_ranking.process_dispatch_param',
                            args=[
                                'activity status',
                                str(event.id) + '|' + change_status_dict[event.event_status]
                            ]) if event.event_status != 'done' else '#'
                    )
                ]
            ),
                             [event for event in events]))
            return BlockObject(status, 'Event', ['Change Status'], event_dict)
        event_api = EventAPI(self.request)
        return BlockSet().makeBlockSet(genDict('future'), genDict('running'), genDict('done'))

    def render(self):
        return super().renderHelper(PageObject('Events List', self.generateList(), []))

    def parseParams(self, param):
        return None
