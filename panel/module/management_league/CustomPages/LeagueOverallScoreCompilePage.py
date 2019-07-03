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

    def genContent(self):
        content = dict()
        league_scoring_list = LeagueScoringAPI(self.request).getFinalLeagueScores()
        for index, data in enumerate(league_scoring_list):
            content[index] = dict(
                league_ranking=data['school_id'],
                school_name=data['school_name'],
                school_score_url=data[''],
                participated_event_num=data['score'],
                league_score=data['base_ranking'],
                league_override_score=data['override_score']
            )
        return content

    def parseParams(self, param):
        super().parseMatch('')
        param = None
        return param
