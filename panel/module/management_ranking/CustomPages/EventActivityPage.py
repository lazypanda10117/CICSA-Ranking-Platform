from django.shortcuts import reverse
from api import EventActivityAPI, EventTagAPI
from ...base.block.CustomPages import AbstractBasePage
from ...base.block.CustomComponents import BlockObject, BlockSet, PageObject


class EventActivityPage(AbstractBasePage):
    def generateList(self):
        def genActivityDict(tag):
            event_activities = event_activity_api.filterSelf(
                event_activity_event_parent=event_id, event_activity_event_tag=tag.id)
            event_activities = sorted(list(event_activities), key=(lambda x: x.event_activity_order))
            event_activity_dict = map(lambda event_activity: dict(
                element_text=event_activity.event_activity_name,
                element_link=reverse(
                    'panel.module.management_ranking.view_dispatch_param',
                    args=['activity ranking', event_activity.id]),
                elements=[
                    dict(
                        text=event_activity.event_activity_status,
                        link='#'
                    )
                ]
            ),
                             [event_activity for event_activity in event_activities])
            return BlockObject(tag.event_tag_name, 'Event Activity', ['Status'], event_activity_dict)

        event_id = int(self.param["id"])
        event_activity_api = EventActivityAPI(self.request)
        event_tag_api = EventTagAPI(self.request)
        blockset = BlockSet().makeBlockSet(
            # event_activity_result
            *[genActivityDict(event_tag) for event_tag in event_tag_api.filterSelf(event_tag_event_id=event_id)]
        )
        return blockset

    def render(self):
        external = dict(
            button=dict(
                link=reverse(
                    'panel.module.management_ranking.view_dispatch_param',
                    args=['compiler', self.param['id']]
                ),
                text='Compile Event'
            )
        )
        return super().renderHelper(PageObject('Event Activities List', self.generateList(), [], external))

    def parseParams(self, param):
        super().parseMatch('\d+')
        param = dict(id=param)
        return param
