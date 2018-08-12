from django.shortcuts import reverse
from blackbox import api
from blackbox.block_app.base.CustomPages import AbstractBasePage
from blackbox.block_app.base.CustomComponents import BlockObject, BlockSet, PageObject

class EventActivityPage(AbstractBasePage):
    def generateList(self):
        def genActivityDict(tag):
            event_activities = event_api.getEventActivities(
                event_activity_event_parent=event_id, event_activity_event_tag=tag.id);
            event_activities = sorted(list(event_activities), key=(lambda x: x.event_activity_order))
            event_activity_dict = map(lambda event_activity: dict(
                element_text=event_activity.event_activity_name,
                element_link=reverse(
                    'blackbox.block_app.management_ranking.view_dispatch',
                    args=['activity ranking', event_activity.id]),
                elements=[
                    dict(
                        text=event_activity.event_activity_status,
                        link='#'
                    )
                ]
            ),
                             [event_activity for event_activity in event_activities]);
            return BlockObject(tag.event_tag_name, 'Event Activity', ['Status'], event_activity_dict);


        event_id = int(self.param);
        event_api = api.EventAPI(self.request);
        blockset = BlockSet().makeBlockSet(
            *[genActivityDict(event_tag) for event_tag in event_api.getEventTags(event_tag_event_id=event_id)] #event_activity_result
        )
        return blockset;

    def render(self):
        return super().renderHelper(PageObject('Event Activities List', self.generateList(), []));