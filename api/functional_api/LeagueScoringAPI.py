import math

from cicsa_ranking.models import Event
from api.base import AbstractCoreAPI
from api.authentication import AuthenticationGuardType
from api.model_api import SchoolAPI, EventAPI, SummaryAPI, ConfigAPI
from api.config import ConfigReader


class LeagueScoringAPI(AbstractCoreAPI):
    def __init__(self, request, season=None):
        super().__init__(request=request, permission=AuthenticationGuardType.PUBLIC_GUARD)
        self.current_configuration = ConfigAPI(self.request).getConfig()
        self.current_season = self.current_configuration.config_current_season
        self.season = self.current_season if season is None else season
        self.LeagueScoringConfig = (ConfigReader('league_scoring').getRootConfig())()
        self.league_scoring_data = self.LeagueScoringConfig.getData('league_rank_place_score_map')

    # TODO: Not supporting getting history league scores yet
    def getCurrentLeagueScoreBySchool(self, school_id):
        school = SchoolAPI(self.request).getSelf(id=school_id)
        events = SchoolAPI(self.request).getParticipatedNormalEvents(school_id, Event.EVENT_STATUS_DONE, self.season)
        # TODO: Optimize the current n x m queries ;_;
        scores = sorted([self.getScoreForEventBySchool(event, school) for event in events], reverse=True)
        average_score = self.getAverageScore(scores, school.school_region)
        final_race_score = self.getFinalRaceScore(school, self.season)
        total_score = average_score + final_race_score
        return total_score

    def getScoreForEventBySchool(self, event, school):
        position = SummaryAPI(self.request).getSummaryRankingBySchool(event.id, school.id)
        return self.getScoreForEvent(position, event.event_team_number, event.event_class)

    def getScoreForEvent(self, position, team_number, event_class):
        try:
            score = self.league_scoring_data.get(event_class).get(team_number).get(position)
        except KeyError:
            raise Exception(
                "Cannot get the score for event given this context. "
                "Event Class: {}  Team Number: {}  Position: {}".format(event_class, team_number, position)
            )
        return score

    def getAverageScore(self, scores, region):
        num_school_in_region = SchoolAPI(self.request).filterSelf(school_region=region).count()
        num_race = len(scores)

        # Specific region has different race num average
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

    # All the functions below corresponds to a specific season (defined by self.season above)
    def setNormalOverrideSummaryScores(self, school, score_dict):
        pass

    def setNormalOverrideLeagueScore(self, school, score_tuple):
        pass

    # Returns either the normal or the overrride score of the summary for the event
    def getCompiledScoreForEvent(self, event, school):
        pass

    # Returns either the normal or the overrride score of the score for the school
    def getFinalLeagueScore(self, school):
        pass

    def getFinalLeagueScores(self):
        pass