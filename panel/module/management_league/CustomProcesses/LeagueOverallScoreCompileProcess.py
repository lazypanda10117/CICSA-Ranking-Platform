from django.shortcuts import redirect, reverse

from misc.CustomFunctions import RequestFunctions
from api.model_api import ConfigAPI
from api.functional_api import LeagueScoringAPI
from panel.module.base.block.CustomProcesses import AbstractBaseProcess


class LeagueOverallScoreCompileProcess(AbstractBaseProcess):
    def process(self):
        post_dict = dict(self.request.POST)
        current_configuration = ConfigAPI(self.request).getConfig()
        current_season = current_configuration.config_current_season
        # school_id = int(RequestFunctions.getSinglePostObj(post_dict, 'school_id_'+str(i)))

        # related_summaries = SummaryAPI(self.request).filterSelf(summary_event_parent=event_id)
        # for i in range(1, int(len(post_dict)/4)+1):
        #     school_id = int(RequestFunctions.getSinglePostObj(post_dict, 'school_id_'+str(i)))
        #     score = int(RequestFunctions.getSinglePostObj(post_dict, 'score_'+str(i)))
        #     ranking = int(RequestFunctions.getSinglePostObj(post_dict, 'ranking_'+str(i)))
        #     override_ranking = int(RequestFunctions.getSinglePostObj(post_dict, 'override_ranking_'+str(i)))
        #     summary_id = related_summaries.get(summary_event_school=school_id).id
        #     result = dict(ranking=ranking, override_ranking=override_ranking, race_score=score)
        #     SummaryAPI(self.request).updateSummaryResult(summary_id, result)
        # EventAPI(self.request).updateEventStatus(event_id, 'done')
        return redirect(
            reverse(
                'panel.module.management_league.view_dispatch',
                args=['overall']
            )
        )

    def parseParams(self, param):
        super().parseMatch('')
        return None
