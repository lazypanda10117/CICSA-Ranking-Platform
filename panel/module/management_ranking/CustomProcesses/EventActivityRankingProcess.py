from django.shortcuts import redirect
from django.shortcuts import reverse

from api.model_api import EventAPI
from api.model_api import EventActivityAPI
from api.functional_api import EventUpdateAPI
from panel.module.base.block.CustomProcesses import AbstractBaseProcess


class EventActivityRankingProcess(AbstractBaseProcess):
    def process(self):
        post_dict = self.post_data
        event_activity_id = int(self.param["id"])
        event_activity_api = EventActivityAPI(self.request)

        event_activity = event_activity_api.getSelf(id=event_activity_id)
        event_activity_parent_id = event_activity.event_activity_event_parent
        event = EventAPI(self.request).getSelf(id=event_activity_parent_id)

        result_dict = {school_id: rank[0] for school_id, rank in post_dict.items()}

        event_activity_api.updateEventActivityResult(event_activity_id, result_dict)
        event_activity_api.updateEventActivityState(event_activity_id, 'done')

        if event.event_status == 'done':
            EventUpdateAPI(self.request, event).recalculateScores()

        return redirect(
            reverse(
                'panel.module.management_ranking.view_dispatch_param',
                args=['activity', event_activity_parent_id]
            )
        )

    def parseParams(self, param):
        super().parseMatch('\d+')
        param = dict(id=param)
        return param
