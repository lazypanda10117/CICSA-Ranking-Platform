from api import SchoolAPI, EventTeamAPI, TeamAPI, MemberGroupAPI
from panel.module.base.block.CustomPages import AbstractBasePage
from panel.module.base.block.CustomComponents import BlockObject, BlockSet, PageObject


class PostPage(AbstractBasePage):
    def generateList(self):
        def genEventTeamDict(activity_id):
            event_teams = event_team_api.filterSelf(event_team_event_activity_id=activity_id)
            event_team_dict = map(lambda event_team: dict(
                element_text=(lambda x: school_api.getSelf(id=x.team_school).school_name + ' - ' + x.team_name)
                (team_api.getSelf(id=event_team.event_team_id)),
                element_link=event_team_api.getEventTeamModifyLink(id=event_team.id),
                elements=[
                    dict(
                        text=member_group_api.getMemberGroupName(event_team.event_team_member_group_id),
                        link=member_group_api.getMemberGroupLink(event_team.event_team_member_group_id)
                    )
                ]
            ),
                             [event_team for event_team in event_teams])
            return BlockObject('Event Teams', 'Event Team', ['Member Group Link'], event_team_dict)

        event_activity_id = int(self.param["id"])
        school_api = SchoolAPI(self.request)
        event_team_api = EventTeamAPI(self.request)
        team_api = TeamAPI(self.request)
        member_group_api = MemberGroupAPI(self.request)
        return BlockSet().makeBlockSet(genEventTeamDict(event_activity_id))

    def render(self):
        return super().renderHelper(PageObject('Event Activity Related Objects List', self.generateList(), []))

    def parseParams(self, param):
        match = super().parseMatch('\d+')
        param = dict(id=param)
        return param
