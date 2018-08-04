from .AbstractDisplayClass import *

from admin_console.generalFunctions import *
from admin_console.HelperClass import *
from admin_console.API import *


class EventActivityDetailDisplay(AbstractDisplayClass):
    def generateList(self):
        def genEventTeamDict(activity_id):
            event_teams = event_activity_api.getEventTeamLinks(event_team_event_activity_id=activity_id);
            event_team_dict = map(lambda event_team: dict(
                element_text=(lambda x: school_api.getSchool(id=x.team_school).school_name + ' - ' + x.team_name)
                (event_activity_api.getEventTeam(id=event_team.event_team_id)),
                element_link='#',
                elements=[
                    dict(
                        text='Modify',
                        link=event_activity_api.getEventTeamModifyLink(id=event_team.id)
                    )
                ]
            ),
                             [event_team for event_team in event_teams]);
            return dict(block_title='Event Teams', element_name='Event Team', header=['Modify'], contents=event_team_dict);
        event_activity_id = int(self.param);
        event_activity_api = EventActivityAPI(self.request);
        school_api = SchoolAPI(self.request);
        event_team_result = {"Event Team": genEventTeamDict(event_activity_id)};
        return event_team_result;

    def render(self):
        return kickRequest(self.request, True, render(
            self.request, 'event_management/eventDisplayList.html',
            {'title': 'Event Activity Related Objects List', 'element_list': self.generateList()}));