import json
from .API import *
from ..generalFunctions import *
from ..models import *

class EventActivityAPI(API):
    def getEventActivity(self, **kwargs):
        return getModelObject(EventActivity, **kwargs);

    def updateEventActivityState(self, event_activity_id, event_activity_status):
        event_activity = getModelObject(EventActivity, id=event_activity_id);
        event_activity.event_activity_status = event_activity_status;
        event_activity.save();

    def updateEventActivityResult(self, event_activity_id, event_activity_result):
        event_activity = getModelObject(EventActivity, id=event_activity_id);
        event_activity.event_activity_result = event_activity_result;
        event_activity.save();

    def getMemberGroupName(self, member_group_id):
        if member_group_id is not None:
            return getModelObject(MemberGroup, id=member_group_id).member_group_name;
        return 'Unlinked';

    def getMemberGroupLink(self, member_group_id):
        if member_group_id is not None:
            return getModifiyLink('member group', id=member_group_id);
        return '#';

    def getEventTeamLinks(self, **kwargs):
        return filterModelObject(EventTeam, **kwargs);

    def getEventTeam(self, **kwargs):
        return getModelObject(Team, **kwargs);

    def getEventActivityModifyLink(self, **kwargs):
        return getModifiyLink('event activity', **kwargs);

    def getEventTeamModifyLink(self, **kwargs):
        return getModifiyLink('event team', **kwargs);