from django.shortcuts import reverse
from api import ScoringPageAPI, EventAPI, EventActivityAPI, SchoolAPI, TeamAPI
from panel.component import CustomElements
from ...base.block.CustomPages import AbstractBasePage


class ScoreCompilingPage(AbstractBasePage):
    DONE = 'done'
    def getPagePath(self):
        return 'platform/module/management_ranking/score_compile.html'

    def render(self):
        return super().renderHelper(self.genPageObject())

    def genPageObject(self):
        return dict(
            block_title='Compile Event',
            action_destination=reverse(
                'panel.module.management_ranking.process_dispatch_param',
                args=['compiler', int(self.param["id"])]),
            form_id='event_compile_form',
            contents=self.genContent()
        )

    def genContent(self):
        def genOptions(data):
            options =  dict()
            for i in range(sum((1 if result['base_ranking'] == data['base_ranking'] else 0) for result in ranking_list)):
                options[i] = dict(
                        disabled=''if data['need_override'] else 'disabled',
                        selected=''if data['need_override'] else 'selected',
                        text=i if data['need_override'] else data['override_ranking']
                )
            return options

        content = dict()
        event_activity_id = int(self.param["id"])
        event_activity = EventActivityAPI(self.request).getSelf(id=event_activity_id)
        event = EventAPI(self.request).getSelf(id=int(event_activity.event_activity_event_parent))
        ranking_list = ScoringPageAPI(self.request).buildDataTable(event)['ranking']
        for index, data in enumerate(ranking_list):
            content[index] = dict(
                school_id=data['school_id'],
                school_name=data['school_name'],
                score=data['score'],
                ranking=data['base_ranking'],
                options=genOptions(data)
            )
        return content

    def parseParams(self, param):
        match = super().parseMatch('\d+')
        param = dict(id=param)
        return param