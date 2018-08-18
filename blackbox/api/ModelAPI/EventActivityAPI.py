from blackbox.api.base.AbstractAPI import AbstractAPI
from misc.GeneralFunctions import generalFunctions as gf
from cicsa_ranking.models import EventActivity, MemberGroup,EventTeam, Team

class EventActivityAPI(AbstractAPI):
    def __init__(self, request):
        super().__init__(request);
        self.base_class = EventActivity;


    def getEventActivity(self, **kwargs):
        return gf.getModelObject(EventActivity, **kwargs);

    def updateEventActivityState(self, event_activity_id, event_activity_status):
        event_activity = gf.getModelObject(EventActivity, id=event_activity_id);
        event_activity.event_activity_status = event_activity_status;
        event_activity.save();

    def updateEventActivityResult(self, event_activity_id, event_activity_result):
        event_activity = gf.getModelObject(EventActivity, id=event_activity_id);
        event_activity.event_activity_result = event_activity_result;
        event_activity.save();

    def getMemberGroupName(self, member_group_id):
        if member_group_id is not None:
            return gf.getModelObject(MemberGroup, id=member_group_id).member_group_name;
        return 'Unlinked';

    def getMemberGroupLink(self, member_group_id):
        if member_group_id is not None:
            return gf.getModifiyLink('member group', id=member_group_id);
        return '#';

    def getEventTeamLinks(self, **kwargs):
        return gf.filterModelObject(EventTeam, **kwargs);

    def getEventTeam(self, **kwargs):
        return gf.getModelObject(Team, **kwargs);

    def getEventActivityModifyLink(self, **kwargs):
        return gf.getModifiyLink('event activity', **kwargs);

    def getEventTeamModifyLink(self, **kwargs):
        return gf.getModifiyLink('event team', **kwargs);