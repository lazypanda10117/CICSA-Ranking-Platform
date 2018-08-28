from api import EventTypeAPI
from ...base.block.CustomPages import AbstractBasePage


class EventChoicePage(AbstractBasePage):
    def getPagePath(self):
        return 'platform/module/management_event/event.html'

    def render(self):
        types = [value.event_type_name for value in EventTypeAPI(self.request).filterSelf()]
        type_style = {'width': int(12 / len(types)) if len(types) else None}
        return super().renderHelper({'types': types, 'type_style': type_style})

    def parseParams(self, param):
        return None
