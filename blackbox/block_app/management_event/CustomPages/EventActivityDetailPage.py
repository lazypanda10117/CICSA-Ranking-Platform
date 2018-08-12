from blackbox import api
from blackbox.block_app.base.CustomPages import AbstractBasePage
from blackbox.block_app.base.CustomComponents import BlockObject, BlockSet, PageObject

class EventActivityDetailPage(AbstractBasePage):
    def generateList(self):
        def genEventTeamDict(activity_id):
            event_teams = event_activity_api.getEventTeamLinks(event_team_event_activity_id=activity_id);
            event_team_dict = map(lambda event_team: dict(
                element_text=(lambda x: school_api.getSchool(id=x.team_school).school_name + ' - ' + x.team_name)
                (event_activity_api.getEventTeam(id=event_team.event_team_id)),
                element_link=event_activity_api.getEventTeamModifyLink(id=event_team.id),
                elements=[
                    dict(
                        text=event_activity_api.getMemberGroupName(event_team.event_team_member_group_id),
                        link=event_activity_api.getMemberGroupLink(event_team.event_team_member_group_id)
                    )
                ]
            ),
                             [event_team for event_team in event_teams]);
            return BlockObject('Event Teams', 'Event Team', ['Member Group Link'], event_team_dict);

        event_activity_id = int(self.param);
        event_activity_api = api.EventActivityAPI(self.request);
        school_api = api.SchoolAPI(self.request);
        return BlockSet().makeBlockSet(genEventTeamDict(event_activity_id));

    def render(self):
        return super().renderHelper(PageObject('Event Activity Related Objects List', self.generateList(), []));