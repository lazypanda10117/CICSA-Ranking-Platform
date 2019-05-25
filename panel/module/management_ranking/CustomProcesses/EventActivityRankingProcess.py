from django.shortcuts import redirect, reverse
from api import EventActivityAPI
from ...base.block.CustomProcesses import AbstractBaseProcess


class EventActivityRankingProcess(AbstractBaseProcess):
    def process(self):
        post_dict = dict(self.request.POST)
        event_activity_id = int(self.param["id"])
        event_activity_api = EventActivityAPI(self.request)

        event_activity = event_activity_api.getSelf(id=event_activity_id)
        event_activity_parent_id = event_activity.event_activity_event_parent
        result_dict = {school_id: rank[0] for school_id, rank in post_dict.items()}
        event_activity_api.updateEventActivityResult(event_activity_id, result_dict)
        event_activity_api.updateEventActivityState(event_activity_id, 'done')

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
