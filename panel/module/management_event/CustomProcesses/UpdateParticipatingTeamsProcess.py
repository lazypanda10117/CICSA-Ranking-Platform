from django.shortcuts import redirect
from django.urls import reverse

from panel.module.base.block.CustomProcesses import AbstractBaseProcess


class UpdateParticipatingTeamsProcess(AbstractBaseProcess):
    def process(self):
        post_dict = dict(self.request.POST)
        # Post Dict Data Example
        # {'event_team_management_checkbox_2': ['on'], 'event_team_management_checkbox_4': ['on'],
        #  'event_team_management_checkbox_5': ['on'], 'event_team_management_checkbox_7': ['on'],
        #  'event_team_management_checkbox_8': ['on'], 'event_team_management_checkbox_9': ['on'],
        #  'event_team_management_checkbox_10': ['on'], 'event_team_management_checkbox_13': ['on'],
        #  'event_team_management_checkbox_14': ['on'], 'event_team_management_checkbox_15': ['on']}
        return redirect(
            reverse(
                'panel.module.management_event.view_dispatch_param',
                args=['team', self.param['id']]
            )
        )

    def parseParams(self, param):
        super().parseMatch('\d+')
        param = dict(id=param)
        return param
