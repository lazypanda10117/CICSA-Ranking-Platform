from .AbstractDisplayClass import *

from admin_console.generalFunctions import *
from admin_console.HelperClass import *
from admin_console.API import *


class EventActivityDisplay(AbstractDisplayClass):
    def generateList(self):
        def genActivityDict(tag):
            event_activities = event_api.getEventActivities(
                event_activity_event_parent=event_id, event_activity_event_tag=tag.id);
            event_activity_dict = map(lambda event_activity: dict(
                element_text=event_activity.event_activity_name,
                element_link=reverse('eventManagementDispatch', args=['activity detail', event_activity.id]),
                elements=[
                    dict(
                        text='Modify',
                        link=event_activity_api.getEventActivityModifyLink(id=event_activity.id)
                    )
                ]
            ),
                             [event_activity for event_activity in event_activities]);
            return dict(block_title=tag.event_tag_name, element_name='Event Activity', header=['Modify'], contents=event_activity_dict);

        def genTagDict(event_id):
            event_tags = event_api.getEventTags(event_tag_event_id=event_id);
            event_tag_dict = map(lambda event_tag: dict(
                element_text=event_tag.event_tag_name,
                element_link=event_api.getEventTagModifyLink(id=event_tag.id),
                elements=[]
            ),
                                      [event_tag for event_tag in event_tags]);
            return dict(block_title='Event Tags', element_name='Event Tag', header=[], contents=event_tag_dict);

        def genSummaryDict(event_id):
            event_summaries = event_api.getEventSummaries(summary_event_parent=event_id);
            event_summary_dict = map(lambda event_summary: dict(
                element_text='Summary - ' + school_api.getSchool(id=event_summary.summary_event_school).school_name,
                element_link=event_api.getEventSummaryModifiyLink(id=event_summary.id),
                elements=[]
            ),
                                      [event_summary for event_summary in event_summaries]);
            return dict(block_title='Event Summaries', element_name='Event Summary', header=[],
                        contents=event_summary_dict);

        def genTeamDict(event_id):
            event_teams = event_api.getEventTeams(event_id);
            event_team_dict = map(lambda event_team: dict(
                element_text=school_api.getSchool(id=event_team.team_school).school_name + ' - ' + event_team.team_name,
                element_link=event_api.getTeamModifyLink(id=event_team.id),
                elements=[]
            ),
                                      [event_team for event_team in event_teams]);
            return dict(block_title='Event Teams', element_name='Event Team', header=[], contents=event_team_dict);

        event_id = int(self.param);
        event_api = EventAPI(self.request);
        event_activity_api = EventActivityAPI(self.request);
        school_api = SchoolAPI(self.request);
        event_activity_result = {event_tag.event_tag_name: genActivityDict(event_tag)
                                 for event_tag in event_api.getEventTags(event_tag_event_id=event_id)};
        event_tag_result = {"Event Tags": genTagDict(event_id)};
        event_summary_result = {"Event Summaries": genSummaryDict(event_id)};
        event_team_result = {"Event Teams": genTeamDict(event_id)};
        return {**event_activity_result, **event_tag_result, **event_summary_result, **event_team_result};

    def render(self):
        return super().renderHelper('Event Related Objects List', self.generateList());