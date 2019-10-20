import random

from cicsa_ranking.models import Team
from cicsa_ranking.models import ScoreMapping
from cicsa_ranking.models import Event
from misc.CustomFunctions import MiscFunctions
from api.base import AbstractCoreAPI
from api.base import SeasonBasedAPI
from api.authentication import AuthenticationGuardType
from api.authentication import AuthenticationActionType
from api.model_api import TeamAPI
from api.model_api import EventTeamAPI
from api.model_api import SchoolAPI
from api.model_api import SummaryAPI
from api.model_api import EventActivityAPI
from api.model_api import EventTagAPI


class EventUpdateAPI(AbstractCoreAPI, SeasonBasedAPI):
    def __init__(self, request, event, **kwargs):
        super().__init__(request=request, permission=AuthenticationGuardType.LOGIN_GUARD, **kwargs)
        self.event = event

    # TODO: Update FleetCreation API to use this new function
    def regenerateRotation(self):
        rotation = dict()
        permutation = random.sample(range(1, self.event.event_team_number + 1), self.event.event_team_number)
        event_tags = EventTagAPI(self.request).verifySelf(legacy=False, event_tag_event_id=self.event.id)
        for boat_shift, tag in enumerate(event_tags):
            teams = TeamAPI(self.request).filterSelf(team_tag_id=tag.id)
            team_sequence = {team.id:
                [
                    MiscFunctions.modAdd(
                        permutation[idx] + boat_shift,
                        (race - race % 2),
                        self.event.event_team_number
                    )
                    for race in range(self.event.event_race_number)
                ]
                for idx, team in enumerate(teams)
            }
            rotation[tag.id] = team_sequence
        return rotation

    def updateSchools(self, school_ids):
        schools = SchoolAPI(self.request).filterSelf(id__in=school_ids)
        # Return error if one or more of the school ids could not be found
        if not len(schools) == len(school_ids):
            raise Exception("At least one of the school ids is invalid in updateSchools")
        old_school_ids = list(map(lambda x: int(x), self.event.event_school_ids))

        # Finding all the elements in school_ids that are not already in old_school_ids, and its converse
        additionList = [e for e in school_ids if e not in old_school_ids]
        removalList = [e for e in old_school_ids if e not in school_ids]

        self.event.event_school_ids = school_ids
        self.event.event_team_number = len(school_ids)
        # Remove some boat identifiers if less schools, or add more non duplicate numbers if more schools
        boat_ids = self.event.event_boat_rotation_name.split(',')
        next_boat_id = (lambda m: m if m is not None else 0)(MiscFunctions.findMaxInStrArr(boat_ids)) + 1
        new_boat_ids = boat_ids[:min(self.event.event_team_number, len(boat_ids))] + \
                                              [str(next_boat_id + i) for i in range(
                                                  max(0, self.event.event_team_number - len(boat_ids))
                                              )]
        self.event.event_boat_rotation_name = ','.join(new_boat_ids)
        self.event.save()

        # Handling Addition first before deletion
        self.updateSummaryBySchool(additionList, AuthenticationActionType.ADD)
        self.updateEventTeams(additionList, AuthenticationActionType.ADD)
        self.updateEventActivities(additionList, AuthenticationActionType.ADD)
        self.updateEventTeamLinks(additionList, AuthenticationActionType.ADD)

        # Handling Deletion
        self.updateSummaryBySchool(removalList, AuthenticationActionType.DELETE)
        self.updateEventActivities(removalList, AuthenticationActionType.DELETE)
        self.updateEventTeamLinks(removalList, AuthenticationActionType.DELETE)
        self.updateEventTeams(removalList, AuthenticationActionType.DELETE)

        # Update rotation, previous doesn't have information about new teams
        self.event.event_rotation_detail = self.regenerateRotation()
        self.event.save()

        # Update Summary and League Scores
        self.recalculateScores()

    def recalculateScores(self):
        from api.client_api import ScoringPageAPI
        from api.functional_api import LeagueScoringAPI

        if self.event.event_status == Event.EVENT_STATUS_DONE:
            ranking_list = ScoringPageAPI(self.request).buildDataTable(self.event, force_compile=True)['ranking']
            summaries = SummaryAPI(self.request).verifySelf(legacy=False, summary_event_parent=self.event.id)
            for ranking_data in ranking_list:
                school_id = ranking_data['school_id']
                score = ranking_data['score']
                base_ranking = ranking_data['base_ranking']
                summary_id = summaries.get(summary_event_school=school_id).id
                # TODO: Take care of override automatically, instead of the hard-coded 0
                result = dict(ranking=base_ranking, override_ranking=0, race_score=score)
                SummaryAPI(self.request).updateSummaryResult(summary_id, result)
        # Recompile league scores if season is finished
        LeagueScoringAPI(self.request).computeLeagueScores(initialize=False)

    def updateSummaryBySchool(self, school_ids, action):
        if action == AuthenticationActionType.ADD:
            for school in school_ids:
                SummaryAPI(self.request).createSelf(
                    summary_event_parent=self.event.id,
                    summary_event_school=school
                )
        elif action == AuthenticationActionType.DELETE:
            SummaryAPI(self.request).deleteSelf(
                legacy=False,
                summary_event_parent=self.event.id,
                summary_event_school__in=school_ids
            ).delete()

    def updateEventTeams(self, school_ids, action):
        event_tags = EventTagAPI(self.request).filterSelf(event_tag_event_id=self.event.id)
        if action == AuthenticationActionType.ADD:
            schools = SchoolAPI(self.request).filterSelf(id__in=school_ids)
            for school in schools:
                for idx, tag in enumerate(event_tags):
                    team_name = '{} {} {}'.format(
                        school.school_default_team_name, Team.TEAM_NAME_SUFFIX, MiscFunctions.getAlphabet(idx)
                    )
                    TeamAPI(self.request).createSelf(
                        team_name=team_name, team_school=school.id, team_status="active", team_tag_id=tag.id
                    )
        elif action == AuthenticationActionType.DELETE:
            TeamAPI(self.request).deleteSelf(
                legacy=False,
                team_tag_id__in=[e.id for e in event_tags],
                team_school__in=school_ids
            ).delete()

    def updateEventActivities(self, school_ids, action):
        event_tags = EventTagAPI(self.request).filterSelf(event_tag_event_id=self.event.id)
        teams = TeamAPI(self.request).filterSelf(
            team_tag_id__in=[e.id for e in event_tags], team_school__in=school_ids
        )
        event_activities = EventActivityAPI(self.request).verifySelf(legacy=False, event_activity_event_parent=self.event.id)
        for activity in event_activities:
            ranking = activity.event_activity_result
            # Don't do anything if ranking is empty, because event is in the future
            if not ranking:
                continue

            # Add/delete the teams specified by school_ids, and commit to db
            for team in teams:
                if action == AuthenticationActionType.ADD:
                    if activity.event_activity_event_tag == team.team_tag_id:
                        ranking.update({team.id: ScoreMapping.DEFAULT_MAPPING})
                elif action == AuthenticationActionType.DELETE:
                    if activity.event_activity_event_tag == team.team_tag_id:
                        ranking.pop(str(team.id))
            # We need to adjust the ranking after deleting some teams
            if action == AuthenticationActionType.DELETE:

                # Ranking sorted by its integer, if it is string like 'DNF', set as 0
                s_ranking = sorted(
                    map(lambda x: x if MiscFunctions.canConvertTo(int, x[1]) else (x[0], -1), ranking.items())
                )
                count = 1
                for team_id, rank in s_ranking:
                    if not rank == -1:
                        ranking.update({team_id: str(count)})
                        count += 1
            activity.event_activity_result = ranking
            activity.save()

    def updateEventTeamLinks(self, school_ids, action):
        event_tags = EventTagAPI(self.request).filterSelf(event_tag_event_id=self.event.id)
        teams = TeamAPI(self.request).filterSelf(
            team_tag_id__in=[e.id for e in event_tags], team_school__in=school_ids
        )
        event_activities = EventActivityAPI(self.request).verifySelf(legacy=False, event_activity_event_parent=self.event.id)
        if action == AuthenticationActionType.ADD:
            for activity in event_activities:
                for team in teams:
                    EventTeamAPI(self.request).createSelf(event_team_event_activity_id=activity.id, event_team_id=team.id)
        elif action == AuthenticationActionType.DELETE:
            EventTeamAPI(self.request).filterSelf(
                event_team_event_activity_id__in=[e.id for e in event_activities],
                event_team_id__in=[t.id for t in teams]
            ).delete()

    def updateRotationByActivity(self, event_activity_id, action):
        def updateIndividualRotation(individual_rotation):
            if action == AuthenticationActionType.ADD:
                if not len(individual_rotation) % 2:
                    individual_rotation.append(
                        MiscFunctions.modAdd(individual_rotation[-1]-1, 2, self.event.event_team_number)
                    )
                else:
                    individual_rotation.append(individual_rotation[-1])
                return individual_rotation
            elif action == AuthenticationActionType.DELETE:
                return individual_rotation[:-1]

        rotation = self.event.event_rotation_detail
        race_tag = EventActivityAPI(self.request).verifySelf(legacy=False, id=event_activity_id).event_activity_race_tag
        team_rotations = rotation[race_tag]
        for team_id, team_rotation in team_rotations.items():
            rotation[race_tag].update(
                dict(
                    team_id=updateIndividualRotation(rotation[race_tag][team_id])
                )
            )
        return rotation

    def updateRaces(self, races):
        # if less, remove some and reorder
        # if more, add
        pass

    def pruneRaces(self):
        # Update Races by deleting all the non-finished ones
        pass
