import random

from api import TeamAPI
from api.base import AbstractCoreAPI
from api.base import SeasonBasedAPI
from api.authentication import AuthenticationGuardType
from api.authentication import AuthenticationActionType
from api.model_api import SchoolAPI
from api.model_api import EventAPI
from api.model_api import SummaryAPI
from api.model_api import ScoreAPI
from api.model_api import EventActivityAPI
from api.model_api import EventTagAPI
from misc.CustomFunctions import MiscFunctions


class EventUpdateAPI(AbstractCoreAPI, SeasonBasedAPI):
    def __init__(self, request, event, **kwargs):
        super().__init__(request=request, permission=AuthenticationGuardType.LOGIN_GUARD, **kwargs)
        self.event = event

    # TODO: Update FleetCreation API to use this new function
    def regenerateRotation(self):
        rotation = dict()
        permutation = random.sample(range(1, self.event.event_team_number + 1), self.event.event_team_number)
        event_tags = EventTagAPI(self.request).verifySelf(event_tag_event_id=self.event.id)
        for boat_shift, tag_id in enumerate(event_tags):
            teams = TeamAPI(self.request).filterSelf(team_tag_id=tag_id)
            team_sequence = { team_id :
                [
                    MiscFunctions.modAdd(
                        permutation[idx] + boat_shift,
                        (race - race % 2),
                        self.event.event_team_number
                    )
                    for race in range(self.event.event_race_number)
                ]
                for idx, team_id in enumerate(teams)
            }
            rotation[tag_id] = team_sequence
        return rotation

    def updateRotationBySchool(self, action):
        if action in [AuthenticationActionType.ADD, AuthenticationActionType.DELETE]:
            return self.regenerateRotation()
        else:
            raise Exception("Error in ActionType for updateRotationBySchool")

    def updateSchools(self, school_ids):
        schools = SchoolAPI(self.request).filterSelf(id__in=school_ids)
        if not len(schools) == len(school_ids):
            raise Exception("At least one of the school ids is invalid in updateSchools")
        self.event.event_school_ids = school_ids
        self.event.event_team_number = len(school_ids)
        # Remove some boat identifiers if less schools, or add more non duplicate numbers if more schools
        boat_ids = self.event.event_boat_rotation_name.split(',')
        next_boat_id = (lambda m: m if m is not None else 0)(MiscFunctions.findMaxInStrArr(boat_ids)) + 1
        self.event.event_boat_rotation_name = boat_ids[:min(self.event.event_team_number, len(boat_ids))] + \
                                              [next_boat_id + i for i in range(
                                                  max(0, self.event.event_team_number - len(boat_ids))
                                              )]
        self.event.save()
        self.updateRotationBySchool()
        # update summary
        self.__updateSummary(self.school)
        # update scores if already compiled

    def __updateSummary(self, school):
        pass

    def updateRotationByActivity(self, event_activity_id, action):
        def updateIndividualRotation(individual_rotation):
            if action == AuthenticationActionType.ADD:
                if not len(individual_rotation) % 2:
                    individual_rotation.append(
                        MiscFunctions.modAdd(
                            individual_rotation[-1]-1,
                            2,
                            self.event.event_team_number
                        )
                    )
                else:
                    individual_rotation.append(individual_rotation[-1])
                return individual_rotation
            elif action == AuthenticationActionType.DELETE:
                return individual_rotation[:-1]
            else:
                raise Exception("Error in ActionType for updateRotationByActivity")

        rotation = self.event.event_rotation_detail
        race_tag = EventActivityAPI(self.request).verifySelf(id=event_activity_id).event_activity_race_tag
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