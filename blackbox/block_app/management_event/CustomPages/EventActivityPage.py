from django.shortcuts import reverse
from blackbox import api
from blackbox.block_app.base.CustomPages import AbstractBasePage
from blackbox.block_app.base.CustomComponents import BlockObject, BlockSet, PageObject


class EventActivityPage(AbstractBasePage):
    def generateList(self):
        def genActivityDict(tag):
            event_activities = event_api.getEventActivities(
                event_activity_event_parent=event_id, event_activity_event_tag=tag.id);
            event_activities = sorted(list(event_activities), key=(lambda x: x.event_activity_order))
            event_activity_dict = map(lambda event_activity: dict(
                element_text=event_activity.event_activity_name,
                element_link=reverse(
                    'blackbox.block_app.management_event.view_dispatch',
                    args=['activity detail', event_activity.id]),
                elements=[
                    dict(
                        text='Modify',
                        link=event_activity_api.getEventActivityModifyLink(id=event_activity.id)
                    )
                ]
            ),
                             [event_activity for event_activity in event_activities]);
            return BlockObject(tag.event_tag_name, 'Event Activity', ['Modify'], event_activity_dict);

        def genTagDict(event_id):
            event_tags = event_api.getEventTags(event_tag_event_id=event_id);
            event_tags = sorted(list(event_tags), key=(lambda x: x.id))
            event_tag_dict = map(lambda event_tag: dict(
                element_text=event_tag.event_tag_name,
                element_link=event_api.getEventTagModifyLink(id=event_tag.id),
                elements=[]
            ),
                                      [event_tag for event_tag in event_tags]);
            return BlockObject('Event Tags', 'Event Tag', [], event_tag_dict);

        def genSummaryDict(event_id):
            event_summaries = event_api.getEventSummaries(summary_event_parent=event_id);
            event_summaries = sorted(list(event_summaries), key=(lambda x: x.id))
            event_summary_dict = map(lambda event_summary: dict(
                element_text='Summary - ' + school_api.getSchool(id=event_summary.summary_event_school).school_name,
                element_link=event_api.getEventSummaryModifiyLink(id=event_summary.id),
                elements=[]
            ),
                                      [event_summary for event_summary in event_summaries]);
            return BlockObject('Event Summaries', 'Event Summary', [], event_summary_dict);

        def genTeamDict(event_id):
            event_teams = event_api.getEventCascadeTeams(event_id);
            event_teams = sorted(list(event_teams), key=(lambda x: x.id))
            event_team_dict = map(lambda event_team: dict(
                element_text=school_api.getSchool(id=event_team.team_school).school_name + ' - ' + event_team.team_name,
                element_link=event_api.getTeamModifyLink(id=event_team.id),
                elements=[]
            ),
                                      [event_team for event_team in event_teams]);
            return BlockObject('Event Teams', 'Event Team', [], event_team_dict);

        event_id = int(self.param["id"]);
        event_api = api.EventAPI(self.request);
        event_activity_api = api.EventActivityAPI(self.request);
        school_api = api.SchoolAPI(self.request);

        blockset = BlockSet().makeBlockSet(
            *[genActivityDict(event_tag) for event_tag in event_api.getEventTags(event_tag_event_id=event_id)], #event_activity_result
            genTagDict(event_id), #event_tag_result
            genSummaryDict(event_id), #event_summary_result
            genTeamDict(event_id) #event_team_result
        )
        return blockset;

    def render(self):
        return super().renderHelper(PageObject('Event Related Objects List', self.generateList(), []));

    def parseParams(self, param):
        match = super().parseMatch('\d+');
        param = dict(id=param);
        return param;