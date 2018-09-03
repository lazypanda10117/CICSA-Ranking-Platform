from django.shortcuts import reverse
from api import EventAPI, EventActivityAPI, EventTagAPI, SchoolAPI, SummaryAPI, TeamAPI
from ...base.block.CustomPages import AbstractBasePage
from ...base.block.CustomComponents import BlockObject, BlockSet, PageObject


class EventActivityPage(AbstractBasePage):
    def generateList(self):
        def genActivityDict(tag):
            event_activities = event_activity_api.filterSelf(
                event_activity_event_parent=event_id, event_activity_event_tag=tag.id)
            event_activities = sorted(list(event_activities), key=(lambda x: x.event_activity_order))
            event_activity_dict = map(lambda event_activity: dict(
                element_text=event_activity.event_activity_name,
                element_link=reverse(
                    'panel.module.management_event.view_dispatch_param',
                    args=['activity detail', event_activity.id]),
                elements=[
                    dict(
                        text='Modify',
                        link=event_activity_api.getEventActivityModifyLink(id=event_activity.id)
                    )
                ]
            ),
                             [event_activity for event_activity in event_activities])
            return BlockObject(tag.event_tag_name, 'Event Activity', ['Modify'], event_activity_dict)

        def genTagDict(event_id):
            event_tags = event_tag_api.filterSelf(event_tag_event_id=event_id)
            event_tags = sorted(list(event_tags), key=(lambda x: x.id))
            event_tag_dict = map(lambda event_tag: dict(
                element_text=event_tag.event_tag_name,
                element_link=event_tag_api.getEventTagModifyLink(id=event_tag.id),
                elements=[]
            ),
                                      [event_tag for event_tag in event_tags])
            return BlockObject('Event Tags', 'Event Tag', [], event_tag_dict)

        def genSummaryDict(event_id):
            event_summaries = summary_api.filterSelf(summary_event_parent=event_id)
            event_summaries = sorted(list(event_summaries), key=(lambda x: x.id))
            event_summary_dict = map(lambda event_summary: dict(
                element_text='Summary - ' + school_api.getSelf(id=event_summary.summary_event_school).school_name,
                element_link=summary_api.getEventSummaryModifiyLink(id=event_summary.id),
                elements=[]
            ),
                                      [event_summary for event_summary in event_summaries])
            return BlockObject('Event Summaries', 'Event Summary', [], event_summary_dict)

        def genTeamDict(event_id):
            event_teams = event_api.getEventCascadeTeams(event_id)
            event_teams = sorted(list(event_teams), key=(lambda x: x.id))
            event_team_dict = map(lambda event_team: dict(
                element_text=school_api.getSelf(id=event_team.team_school).school_name + ' - ' + event_team.team_name,
                element_link=team_api.getTeamModifyLink(id=event_team.id),
                elements=[]
            ),
                                      [event_team for event_team in event_teams])
            return BlockObject('Event Teams', 'Event Team', [], event_team_dict)

        event_id = int(self.param["id"])
        event_api = EventAPI(self.request)
        event_activity_api = EventActivityAPI(self.request)
        event_tag_api = EventTagAPI(self.request)
        school_api = SchoolAPI(self.request)
        summary_api = SummaryAPI(self.request)
        team_api = TeamAPI(self.request)

        blockset = BlockSet().makeBlockSet(
            *[
                genActivityDict(event_tag)
                for event_tag in
                event_tag_api.filterSelf(event_tag_event_id=event_id)
            ],  # event_activity_result
            genTagDict(event_id),  # event_tag_result
            genSummaryDict(event_id),  # event_summary_result
            genTeamDict(event_id)  # event_team_result
        )
        return blockset

    def render(self):
        return super().renderHelper(PageObject('Event Related Objects List', self.generateList(), []))

    def parseParams(self, param):
        match = super().parseMatch('\d+')
        param = dict(id=param)
        return param
