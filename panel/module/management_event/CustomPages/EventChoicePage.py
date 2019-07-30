from django.urls import reverse

from api import EventTypeAPI
from panel.module.base.block.CustomPages import AbstractBasePage


class EventChoicePage(AbstractBasePage):
    def getPagePath(self):
        return 'platform/module/management_event/event.html'

    def genPageObject(self):
        # We are ignoring team racing for active types right now because that is still WIP
        active_types = EventTypeAPI(self.request).getAll().filter(event_type_name='fleet')
        wip_types = EventTypeAPI(self.request).getAll().filter(event_type_name='team')
        contents = list()
        for event_type in active_types:
            type_name = event_type.event_type_name
            contents.append(
                dict(
                    event_type=type_name,
                    destination=reverse(
                        'panel.module.management_event.view_dispatch_param',
                        args=['event', type_name]
                    )
                )
            )
        for event_type in wip_types:
            type_name = event_type.event_type_name + ' (WIP)'
            contents.append(
                dict(
                    event_type=type_name,
                    destination='#'
                )
            )
        return dict(block_title='Event Types', contents=contents)

    def render(self):
        return super().renderHelper(self.genPageObject())

    def parseParams(self, param):
        return None
