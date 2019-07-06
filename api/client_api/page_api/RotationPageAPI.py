from api.base.GeneralClientAPI import GeneralClientAPI
from api.client_api.page_api.ScoringPageAPI import ScoringPageAPI
from api.model_api import SchoolAPI
from api.model_api import EventAPI
from api.model_api import EventTagAPI
from api.model_api import TeamAPI


class RotationPageAPI(GeneralClientAPI):
    def getEventDetails(self, event_id):
        return ScoringPageAPI(self.request).getEventDetails(event_id)

    def buildEventDetailsDict(self, event):
        return ScoringPageAPI(self.request).buildEventDetailsDict(event)

    def __buildRotationTable(self, event):
        rotation_detail = event.event_rotation_detail
        boat_identifiers = event.event_boat_rotation_name.split(',')
        rotation_table = dict()
        schools = SchoolAPI(self.request).filterSelf(id__in=list(map(lambda x: int(x), event.event_school_ids)))
        teams = EventAPI(self.request).getEventCascadeTeams(event.id)
        team_flatten_ids = [team.id for team in teams]
        team_school_link = dict()
        team_name_link = dict()
        for team in TeamAPI(self.request).filterSelf(id__in=team_flatten_ids):
            team_school_link[team.id] = schools.get(id=team.team_school)
            team_name_link[team.id] = team_school_link[team.id].school_name + ' - ' + team.team_name
        for event_tag_id, teams in rotation_detail.items():
            event_tag_name = EventTagAPI(self.request).getSelf(id=event_tag_id).event_tag_name
            rotation_table[event_tag_name] = dict()
            for team_id, rotations in teams.items():
                team_id = int(team_id)
                rotation_table[event_tag_name][team_id] = dict()
                rotation_table[event_tag_name][team_id]['team_name'] = team_name_link[team_id]
                rotation_table[event_tag_name][team_id]['rotations'] = [
                    boat_identifiers[int(r_num)-1] for r_num in rotations
                ]
        return dict(rotation_table)

    def grabPageData(self, **kwargs):
        event_id = kwargs['id']
        event = self.getEventDetails(event_id)
        event_details = self.buildEventDetailsDict(event)
        rotation_table = self.__buildRotationTable(event)
        page_data = dict(
            event_details=event_details,
            rotation_details=rotation_table
        )
        return page_data
