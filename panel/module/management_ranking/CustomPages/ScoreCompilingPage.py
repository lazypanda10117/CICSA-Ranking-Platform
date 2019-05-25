from django.shortcuts import reverse
from api import ScoringPageAPI, EventAPI
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
            if event.event_status != "done":
                for i in range(sum((1 if result['base_ranking'] == data['base_ranking'] else 0) for result in ranking_list)):
                    options[i] = dict(
                            disabled='',
                            selected=''if data['need_override'] else 'selected',
                            text=i if data['need_override'] else data['override_ranking']
                    )
            else:
                for i in range(sum((1 if result['base_ranking'] == data['base_ranking'] else 0) for result in ranking_list)):
                    options[i] = dict(
                            disabled='',
                            selected='selected' if (i == int(data['override_ranking']) or not data['need_override']) else '',
                            text=i if data['need_override'] else data['override_ranking']
                    )
            return options

        content = dict()
        event_id = int(self.param["id"])
        event = EventAPI(self.request).getSelf(id=event_id)
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
        super().parseMatch('\d+')
        param = dict(id=param)
        return param