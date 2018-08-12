from blackbox import api
from blackbox.block_app.base.CustomPages import AbstractBasePage

class EventChoicePage(AbstractBasePage):
    def getPagePath(self):
        return 'console/event.html';

    def render(self):
        types = [value.event_type_name for value in api.EventAPI(self.request).getEventTypes()];
        type_style = {'width': int(12 / len(types)) if len(types) else None}
        return super().renderHelper({'types': types, 'type_style': type_style});