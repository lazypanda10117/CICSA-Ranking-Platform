import math
from functools import reduce

from cicsa_ranking.models import Event
from cicsa_ranking.models import Summary
from cicsa_ranking.models import Score
from api.base import AbstractCoreAPI
from api.base import SeasonBasedAPI
from api.model_api import SchoolAPI
from api.model_api import EventAPI
from api.model_api import SummaryAPI
from api.model_api import ScoreAPI
from api.config import ConfigReader


class LeagueScoringAPI(AbstractCoreAPI, SeasonBasedAPI):
    def __init__(self, request, season=None):
        super().__init__(request=request, season=season)
        self.LeagueScoringConfig = (ConfigReader('league_scoring').getRootConfig())()
        self.league_scoring_data = self.LeagueScoringConfig.getData('league_rank_place_score_map')

    # TODO: Not supporting getting history league scores yet
    def getCurrentLeagueScoreBySchool(self, school_id, compiled=False, subcompiled=False):
        school = SchoolAPI(self.request).getSelf(id=school_id)
        if compiled:
            return self.getCompiledScoreForSchool(school, error=False)
        else:
            events = SchoolAPI(self.request).getParticipatedNormalEvents(
                school_id,
                Event.EVENT_STATUS_DONE,
                self.season
            )
            # TODO: Optimize the current n x m queries ;_;
            scores = [score for score, event in self.getReverseSortedEventScoresList(school, events, subcompiled)]
            average_score = self.getAverageScore(scores, school.school_region)
            final_race_score = self.getFinalRaceScore(school, self.season)
            total_score = average_score + final_race_score
            return total_score

    def getReverseSortedEventScoresList(self, school, events, subcompiled=False):
        return sorted(
            [(self.getScoreForEventBySchool(event, school, subcompiled), event) for event in events],
            key=lambda eventTuple: (eventTuple[0], eventTuple[1].event_create_time),
            reverse=True
        )

    # Returns either the normal or the overrride score of the summary for the event
    def getCompiledScoreForSchool(self, school, error=True):
        score = ScoreAPI(self.request).getSeasonScoreValue(school.id, season_id=self.season)
        if score == Score.DEFAULT_LEAGUE_SCORE:
            if error:
                raise Exception(
                    "Cannot invoke getCompiledScoreForSchool without first compiling"
                    " the scores for the school (id: {})".format(school.id)
                )
            else:
                return None
        return score

    def getScoreForEventBySchool(self, event, school, compiled):
        if compiled:
            try:
                return self.getCompiledScoreForEventBySchool(event, school)
            except Exception as e:
                pass
        position = SummaryAPI(self.request).getSummaryRankingBySchool(event.id, school.id)
        return self.getScoreForEvent(position, event.event_team_number, event.event_class)

    def getScoreForEvent(self, position, team_number, event_class):
        try:
            score = self.league_scoring_data.get(str(event_class)).get(str(team_number)).get(str(position))
        except KeyError:
            raise Exception(
                "Cannot get the score for event given this context. "
                "Event Class: {}  Team Number: {}  Position: {}".format(event_class, team_number, position)
            )
        return score

    # Returns either the normal or the overrride score of the summary for the event
    def getCompiledScoreForEventBySchool(self, event, school):
        def isScoreCompiled(summary):
            return not summary.summary_event_ranking == Summary.DEFAULT_SUMMARY_LEAGUE_SCORE

        summary = SummaryAPI(self.request).getSelf(summary_event_parent=event.id, summary_event_school=school.id)
        if isScoreCompiled(summary):
            raise Exception(
                "Cannot invoke getCompiledScoreForEvent without first compiling"
                " the scores for the event (id: {}) and school (id: {})".format(event.id, school.id)
            )
        return summary.summary_event_league_score \
            if summary.summary_event_override_league_score == Summary.DEFAULT_SUMMARY_LEAGUE_SCORE \
            else summary.summary_event_override_league_score

    def getAverageFactor(self, region, num_race):
        num_school_in_region = SchoolAPI(self.request).filterSelf(school_region=region).count()
        # Specific region has different race num average
        if num_school_in_region in [1, 2]:
            base_average_race_num = 1
        elif num_school_in_region >= 3:
            base_average_race_num = 3
        else:
            raise Exception("Try to retrieve a region with less than or equal to 0 school.")

        average_factor = max(base_average_race_num, min(math.ceil(num_race/2), 4))
        return average_factor

    def getAverageScore(self, scores, region):
        num_race = len(scores)
        average_factor = self.getAverageFactor(region, num_race)
        total_score = 0
        for count, score in enumerate(scores):
            if count < average_factor:
                total_score += score
            else:
                break
        return total_score/average_factor

    def getFinalRaceScore(self, school, season):
        final_event = EventAPI(self.request).getSelf(event_name__in=Event.EVENT_NAME_FINAL_RACE, event_season=season)
        if final_event and final_event.event_status == Event.EVENT_STATUS_DONE:
            final_ranking = SummaryAPI(self.request).getSummaryRankingBySchool(final_event.id, school.id)
            if final_ranking is not None:
                return self.getScoreForEvent(final_ranking, final_event.event_team_number, final_event.event_class)
        return 0

    def setNormalOverrideSummaryScores(self, school, score_dict):
        school_id = school.id
        for event_id, score in score_dict.items():
            summary = SummaryAPI(self.request).verifySelf(summary_event_parent=event_id, summary_event_school=school_id)
            summary.summary_event_league_score = float(score)
            summary.save()

    def setNormalOverrideLeagueScore(self, school, score_tuple):
        school_id = school.id
        score = ScoreAPI(self.request).getSelf(score_school=school_id, score_season=self.season)
        if score is None:
            score = Score()
            score.score_school = school_id
            score.score_season = self.season
            score.score_value = float(score_tuple[0])
            score.score_override_value = float(score_tuple[1])
            ScoreAPI(self.request).addSelf(score)
            score.save()
        else:
            score.score_value = float(score_tuple[0])
            score.score_override_value = float(score_tuple[1])
            ScoreAPI(self.request).verifySelf(id=score.id)
            score.save()

    def getPanelLeagueScoreData(self):
        schools = SchoolAPI(self.request).getAll()
        result = list()
        for school in schools:
            school_id = school.id
            school_name = school.school_name
            participated_events = SchoolAPI(self.request).getParticipatedEvents(
                school_id,
                Event.EVENT_STATUS_DONE,
                self.season
            )
            participated_events_num = participated_events.count()
            calculated_score = self.getCurrentLeagueScoreBySchool(school_id=school.id, compiled=False)
            recorded_score = self.getCurrentLeagueScoreBySchool(school_id=school.id, compiled=True)
            response = dict(
                school_id=school_id,
                school_name=school_name,
                participated_events_num=participated_events_num,
                calculated_score=calculated_score,
                recorded_score=recorded_score,
            )
            result.append(response)
        return result

    def tryCompileThenCalculateScore(self, school):
        try:
            return self.getCompiledScoreForSchool(school, error=True)
        except:
            return self.getCurrentLeagueScoreBySchool(school_id=school.id, compiled=False)

    def getClientLeagueScoreData(self):
        schools = SchoolAPI(self.request).getAll()
        result = list()
        for school in schools:
            compiled = True
            school_id = school.id
            school_name = school.school_name
            score = self.getCompiledScoreForSchool(school, error=False)
            if score is None:
                compiled = False
                score = self.tryCompileThenCalculateScore(school)
            response = dict(
                compiled=compiled,
                school_id=school_id,
                school_name=school_name,
                display_score=score,
                num_race=SchoolAPI(self.request).getParticipatedEvents(
                        school_id=school_id,
                        status=Event.EVENT_STATUS_DONE,
                        season=self.season,
                    ).count()
            )
            result.append(response)
        return result

    # override is a n-vector of 2-tuples (school id, override value)
    def computeLeagueScores(self, initialize=True, override=None):
        league_scoring_data = self.getPanelLeagueScoreData()
        league_scoring_map = {
            data.get('school_id'): data
            for data in league_scoring_data
        }

        # TODO: Have an indicator for finished season and use it to determine whether to recompile league scores
        # We only recompute if initialize is true and all recorded scores are not None
        if not (initialize or reduce(lambda x, y: x and (y['recorded_score'] is not None), league_scoring_data, True)):
            print("I AM HOME!")
            return

        # We initialize override as all None values if the override variable is not set
        if override is None:
            override = [(school_id, False) for school_id in league_scoring_map.keys()]

        # Update the DB according to override values, otherwise, compute the calculated values again
        for school_id, override_score in override:
            league_scoring_api = LeagueScoringAPI(self.request)
            school_id = int(school_id)
            school = SchoolAPI(self.request).getSelf(id=school_id)
            calculated_score = league_scoring_map.get(school_id).get('calculated_score')
            if not override_score:
                override_score = Score.DEFAULT_LEAGUE_SCORE
            participated_events = SchoolAPI(self.request).getParticipatedEvents(
                school_id,
                Event.EVENT_STATUS_DONE,
                self.season
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
