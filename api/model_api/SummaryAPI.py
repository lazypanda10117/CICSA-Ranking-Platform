from cicsa_ranking.models import Summary
from misc.CustomFunctions import AuthFunctions, LogFunctions, UrlFunctions
from api.base.GeneralModelAPI import GeneralModelAPI


class SummaryAPI(GeneralModelAPI):
    @staticmethod
    def getBaseClass():
        return Summary

    def updateSummaryResult(self, summary_id, result):
        summary = self.verifySelf(id=summary_id)
        AuthFunctions.raise404Empty(summary)
        summary.summary_event_ranking = result['ranking']
        summary.summary_event_override_ranking = result['override_ranking']
        summary.summary_event_race_score = result['race_score']
        summary.summary_event_league_score = 0.0
        summary.summary_event_override_league_score = 0.0
        summary.save()
        LogFunctions.generateLog(self.request, 'admin', LogFunctions.makeLogQuery(Summary, 'Edit', id=summary.id))

    @staticmethod
    def getEventSummaryModifiyLink(**kwargs):
        return UrlFunctions.getModifyLink('summary', **kwargs) + '&base=event_mgmt'

    def getSummaryRankingBySchool(self, event_id, school_id):
        summary = self.getSelf(summary_event_parent=event_id, summary_event_school=school_id)
        if summary:
            return summary.summary_event_ranking + summary.summary_event_override_ranking
        else:
            return -1