from cicsa_ranking.models import Event
from misc.CustomFunctions import AuthFunctions, LogFunctions, UrlFunctions
from ..base.GeneralModelAPI import GeneralModelAPI
from ..model_api import EventActivityAPI, EventTeamAPI, TeamAPI


class EventAPI(GeneralModelAPI):
    def setBaseClass(self):
        return Event;

    def getEventCascadeTeams(self, event_id):
        event_activity_api = EventActivityAPI(self.request);
        event_team_api = EventTeamAPI(self.request);
        team_api = TeamAPI(self.request);
        event_activities = list(map(lambda x: x.id,
                                    event_activity_api.filterSelf(event_activity_event_parent=event_id)));
        event_teams = list(map(lambda x: x.event_team_id, event_team_api.filterSelf(event_team_event_activity_id__in=event_activities).distinct('event_team_id')));
        teams = team_api.filterSelf(id__in=event_teams);
        return teams;

    def updateEventStatus(self, event_id, event_status):
        event = self.getSelf(id=event_id);
        AuthFunctions.raise404Empty(event);
        event.event_status = event_status;
        event.save();
        LogFunctions.loghelper(self.request, 'admin', gf.logQueryMaker(Event, 'Edit', id=event.id))

    @staticmethod
    def getEventModifyLink(self, event_type, **kwargs):
        return UrlFunctions.getModifiyLink(event_type, **kwargs);
