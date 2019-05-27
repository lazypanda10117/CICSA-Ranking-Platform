import math

from cicsa_ranking.models import Event
from api.base import AbstractCoreAPI
from api.model_api import SchoolAPI, EventAPI, SummaryAPI, ConfigAPI


class LeagueScoringAPI(AbstractCoreAPI):
    LEAGUE_SCORE_AVERAGE_COUNT = 3

    # TODO: Not supporting getting history league scores yet
    def getCurrentLeagueScoreBySchool(self, school_id):
        current_configuration = ConfigAPI(self.request).getAll()[0]
        current_season = current_configuration.config_current_season
        school = SchoolAPI(self.request).getSelf(id=school_id)
        events = SchoolAPI(self.request).getParticipatedNormalEvents(school_id, Event.EVENT_STATUS_DONE, current_season)
        # TODO: Optimize the current n x m queries ;_;
        scores = sorted([self.getScoreForEventBySchool(event, school) for event in events], reverse=True)
        average_score = self.getAverageScore(scores, school.school_region)
        final_race_score = self.getFinalRaceScore(school, current_season)
        total_score = average_score + final_race_score
        return total_score

    def getScoreForEventBySchool(self, event, school):
        position = SummaryAPI(self.request).getSummaryRankingBySchool(event.id, school.id)
        return self.getScoreForEvent(position, event.event_team_number, event.event_class)

    def getScoreForEvent(self, position, team_number, event_class):
        # A multivariate function that takes in 3 variables and return the score
        return 0

    def getAverageScore(self, scores, region):
        num_school_in_region = SchoolAPI(self.request).filterSelf(school_region=region).count()
        num_race = len(scores)

        if num_school_in_region in [1, 2]:
            base_average_race_num = 1
        elif num_school_in_region >= 3:
            base_average_race_num = 3
        else:
            raise Exception("Try to retrieve a region with less than or equal to 0 school.")

        average_factor = max(base_average_race_num, min(math.ceil(num_race/2), 4))

        total_score = 0
        for count, score in enumerate(scores):
            if count < average_factor:
                total_score += score
            else:
                break
        return total_score/average_factor

    def getFinalRaceScore(self, school, season):
        final_event = EventAPI(self.request).getSelf(event_name__in=Event.EVENT_NAME_FINAL_RACE, event_season=season)
        final_ranking = SummaryAPI(self.request).getSummaryRankingBySchool(final_event.id, school.id)
        if final_event and final_event.event_status == Event.EVENT_STATUS_DONE:
            return self.getScoreForEvent(final_ranking, final_event.event_team_number, final_event.event_class)
        else:
            return 0
