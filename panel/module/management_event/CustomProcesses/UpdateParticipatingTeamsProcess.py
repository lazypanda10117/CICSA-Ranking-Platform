from django.shortcuts import redirect
from django.urls import reverse

from api.model_api import EventAPI
from api.functional_api import EventUpdateAPI
from panel.module.base.block.CustomProcesses import AbstractBaseProcess


class UpdateParticipatingTeamsProcess(AbstractBaseProcess):
    def process(self):
        post_dict = dict(self.request.POST)
        # Post Dict Data Example
        # {'event_team_management_checkbox-2': ['on']}
        event_id = self.param['id']
        event = EventAPI(self.request).getSelf(id=event_id)
        school_ids = [int(name.split('-')[1]) for name in post_dict.keys()]
        EventUpdateAPI(self.request, event).updateSchools(school_ids)
        return redirect(
            reverse(
                'panel.module.management_event.view_dispatch_param',
                args=['team', event_id]
            )
        )

    def parseParams(self, param):
        super().parseMatch('\d+')
        param = dict(id=param)
        return param
