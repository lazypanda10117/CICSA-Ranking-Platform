from django.urls import reverse

from api.functional_api import LeagueScoringAPI
from panel.module.base.block.CustomPages import AbstractBasePage


class LeagueOverallScoreCompilePage(AbstractBasePage):
    def getPagePath(self):
        return 'platform/module/management_league/overall_compile.html'

    def render(self):
        return super().renderHelper(self.genPageObject())

    def genPageObject(self):
        return dict(
            block_title='Compile League Overall Score',
            action_destination=reverse(
                'panel.module.management_league.process_dispatch',
                args=['overall_compiler']),
            form_id='league_overall_compile_form',
            contents=self.genContent()
        )

    # TODO: transform school id to the edit page for the league score of that school
    def schoolUrlTransformer(self, school_id):
        return school_id

    def genContent(self):
        content = dict()
        league_scoring_list = LeagueScoringAPI(self.request).getPanelLeagueScoreData()
        for index, data in enumerate(league_scoring_list):
            content[index] = dict(
                school_name=data['school_name'],
                school_score_url=self.schoolUrlTransformer(data['school_id']),
                participated_event_num=data['participated_event_num'],
                league_calculated_score=data['calculated_score'],
                league_recorded_score=data['recorded_score'],
            )
        content_list = [(idx, o) for idx, o in enumerate(sorted(content.values(), key=lambda x: x.calculated_score))]
        return content_list

    def parseParams(self, param):
        super().parseMatch('')
        param = None
        return param
