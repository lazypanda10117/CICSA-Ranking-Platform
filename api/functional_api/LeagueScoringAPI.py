from cicsa_ranking.models import Event
from api.base import AbstractCoreAPI
from api.model_api import SchoolAPI, EventAPI, SummaryAPI, ConfigAPI


class LeagueScoringAPI(AbstractCoreAPI):
    LEAGUE_SCORE_AVERAGE_COUNT = 3

    # TODO: Not supporting getting history league scores yet
    def getCurrentLeagueScoreBySchool(self, school_id):
        current_configuration = ConfigAPI(self.request).getAll()[0]
        current_season = current_configuration.config_current_season
        events = SchoolAPI(self.request).getParticipatedEvents(school_id, Event.EVENT_STATUS_DONE, current_season)
        # TODO: Optimize the current n x m queries ;_;
        scores = sorted([self.getScoreForEventBySchool(event.id, school_id) for event in events], reverse=True)
        average_score = self.getAverageScore(scores)
        final_race_score = self.getFinalRaceScore(school_id, current_season)
        total_score = average_score + final_race_score
        return total_score

    def getScoreForEventBySchool(self, event_id, school_id):
        event = EventAPI(self.request).getSelf(id=event_id)
        position = SummaryAPI(self.request).getSummaryRankingBySchool(event.id, school_id)
        return self.getScoreForEvent(position, event.event_team_number, event.event_class)

    def getScoreForEvent(self, position, team_number, event_class):
        # A multivariate function that takes in 3 variables and return the score
        return 0

    def getAverageScore(self, scores):
        total_score = 0
        for count, score in enumerate(scores):
            if count < self.LEAGUE_SCORE_AVERAGE_COUNT:
                total_score += score
            else:
                break
        return total_score/self.LEAGUE_SCORE_AVERAGE_COUNT

    def getFinalRaceScore(self, school_id, season):
        final_event = EventAPI(self.request).getSelf(event_name__in=Event.EVENT_NAME_FINAL_RACE, event_season=season)
        final_ranking = SummaryAPI(self.request).getSummaryRankingBySchool(final_event.id, school_id)
        if final_event and final_event.event_status == Event.EVENT_STATUS_DONE:
            return self.getScoreForEvent(final_ranking, final_event.event_team_number, final_event.event_class)
        else:
            return 0
