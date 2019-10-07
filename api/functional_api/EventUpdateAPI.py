from api.base import AbstractCoreAPI
from api.base import SeasonBasedAPI
from api.authentication import AuthenticationGuardType
from api.model_api import SchoolAPI
from api.model_api import EventAPI
from api.model_api import SummaryAPI
from api.model_api import ScoreAPI
from api.model_api import EventActivityAPI
from api.model_api import EventTagAPI


class EventUpdateAPI(AbstractCoreAPI):
    def __init__(self, request, event, **kwargs):
        super().__init__(request=request, permission=AuthenticationGuardType.LOGIN_GUARD, **kwargs)
        self.event = event

    def recompileEvent(self):


    def __updateRotation(self):
        event_tags = EventTagAPI(self.request).filterSelf(event_tag_event_id=self.event.id)
        event_tags = sorted(list(event_tags), key=(lambda x: x.id))

        event_activities = EventActivityAPI(self.request).filterSelf(
            event_activity_event_parent=self.event.id, event_activity_event_tag=tag.id)
        event_activities = sorted(list(event_activities), key=(lambda x: x.event_activity_order))

        event_summaries = SummaryAPI(self.request).filterSelf(summary_event_parent=self.event.id)
        event_summaries = sorted(list(event_summaries), key=(lambda x: x.id))

        event_teams = EventAPI(self.request).getEventCascadeTeams(self.event.id)
        event_teams = sorted(list(event_teams), key=(lambda x: x.id))
        pass

    def updateTeams(self, teams):
        # update rotation
        self.__updateRotation()
        # update summary
        self.__updateSummary(self.school)
        # update scores if already compiled
        pass

    def __updateSummary(self, school):


    def updateRaces(self, races):
        # if less, remove some and reorder
        # if more, add
        pass

    def pruneRaces(self):
        # Update Races by deleting all the non-finished ones
        pass