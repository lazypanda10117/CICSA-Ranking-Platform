from django.shortcuts import reverse

from panel.module.base.block.CustomPages import AbstractBasePage
from api.model_api import EventAPI
from api.model_api import SchoolAPI


class EventTeamPage(AbstractBasePage):
    def getPagePath(self):
        return 'platform/module/management_event/event_team.html'

    def render(self):
        return super().renderHelper(self.genPageObject())

    def genPageObject(self):
        event_id = self.param["id"]
        return dict(
            block_title='Event Team Management',
            action_destination=reverse(
                'panel.module.management_event.process_dispatch_param',
                args=['update teams', event_id]),
            form_id='event_team_update_form',
            contents=self.genContent(event_id)
        )

    def genContent(self, event_id):
        content = dict()
        event = EventAPI(self.request).getSelf(id=event_id)
        schools = SchoolAPI(self.request).getAll()
        participating_school_ids = [int(school_id) for school_id in event.event_school_ids]
        for idx, school in enumerate(schools):
            content[idx] = dict(
                school_id=school.id,
                school_url=reverse(
                    'client.view_dispatch_param',
                    args=['school_specific', school.id]
                ),
                school_name=school.school_name,
                participated=school.id in participating_school_ids,
            )
        content_list = [
            v for v in sorted(
                content.values(),
                key=lambda x: (x['participated'], -x['school_id']),
                reverse=True
            )
        ]
        return content_list

    def parseParams(self, param):
        super().parseMatch('\d+')
        param = dict(id=param)
        return param
