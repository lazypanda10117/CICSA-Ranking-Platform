from django.shortcuts import redirect
from django.shortcuts import reverse

from cicsa_ranking.models import Event
from cicsa_ranking.models import Score
from misc.CustomFunctions import RequestFunctions
from panel.module.base.block.CustomProcesses import AbstractBaseProcess
from api import ConfigAPI
from api import SchoolAPI
from api import LeagueScoringAPI


class LeagueOverallScoreCompileProcess(AbstractBaseProcess):
    def process(self):
        post_dict = dict(self.request.POST)
        current_configuration = ConfigAPI(self.request).getConfig()
        current_season = current_configuration.config_current_season
        league_scoring_map = {
            data.get('school_id') : data
            for data in LeagueScoringAPI(self.request).getPanelLeagueScoreData()
        }
        # update the db according to override values, otherwise, compute the calculated values again
        for school_id, element in post_dict.items():
            league_scoring_api = LeagueScoringAPI(self.request)
            school_id = int(school_id)
            school = SchoolAPI(self.request).getSelf(id=school_id)
            override_score = element[0]
            calculated_score = league_scoring_map.get(school_id).get('calculated_score')
            if not override_score:
                override_score = Score.DEFAULT_LEAGUE_SCORE
            participated_events = SchoolAPI(self.request).getParticipatedEvents(
                school_id,
                Event.EVENT_STATUS_DONE,
                current_season
            )
            school_score_dict = {
                event.id: league_scoring_api.getScoreForEventBySchool(
                    event, school, False
                ) for event in participated_events
            }
            league_scoring_api.setNormalOverrideLeagueScore(
                school, (calculated_score, override_score)
            )
            league_scoring_api.setNormalOverrideSummaryScores(
                school, school_score_dict
            )
        return redirect(
            reverse(
                'panel.module.management_league.view_dispatch',
                args=['overall']
            )
        )

    def parseParams(self, param):
        super().parseMatch('')
        param = None
        return param