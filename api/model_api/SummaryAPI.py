from cicsa_ranking.models import Event
from cicsa_ranking.models import Summary
from misc.CustomFunctions import AuthFunctions
from misc.CustomFunctions import LogFunctions 
from misc.CustomFunctions import UrlFunctions
from api.base.GeneralModelAPI import GeneralModelAPI
from api.model_api.ConfigAPI import ConfigAPI
from api.model_api.SchoolAPI import SchoolAPI

class SummaryAPI(GeneralModelAPI):
    @staticmethod
    def getBaseClass():
        return Summary

    def updateSummaryResult(self, summary_id, result):
        summary = self.editSelf(id=summary_id)
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
        return self.getSummaryRankingBySummary(summary)

    def getSummaryRankingBySummary(self, summary):
        if not summary:
            return None
        if summary.summary_event_ranking == Summary.DEFAULT_SUMMARY_LEAGUE_SCORE:
            return None
        else:
            return summary.summary_event_ranking + summary.summary_event_override_ranking
        
    def getAllSummaryRankingBySchool(self, school_id, season=None):
        if season is None:
            season = ConfigAPI(self.request).getConfig().config_current_season
        events = SchoolAPI(self.request).getParticipatedEvents(
            school_id,
            Event.EVENT_STATUS_DONE,
            season
        )
        summaries = self.filterSelf(
            summary_event_school=school_id, 
            summary_event_parent__in=[event.id for event in events]
        )
        return {
                    summary.summary_event_parent: self.getSummaryRankingBySummary(summary) 
                    for summary in summaries
                }
