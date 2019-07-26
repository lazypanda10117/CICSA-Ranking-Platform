from django.urls import reverse

from api import EventTypeAPI
from panel.module.base.block.CustomPages import AbstractBasePage


class EventChoicePage(AbstractBasePage):
    def getPagePath(self):
        return 'platform/module/management_event/event.html'

    def render(self):
        return super().renderHelper(self.genPageObject())

    def genPageObject(self):
        types = EventTypeAPI(self.request).getAll()
        contents = list()
        for event_type in types:
            type_name = event_type.event_type_name
            contents.append(dict(
                event_type=type_name,
                destination=reverse(
                    'panel.module.management_event.view_dispatch_param',
                    args=['event', type_name]
                )
            ))
        return dict(block_title='Event Types', contents=contents)

    def parseParams(self, param):
        return None
