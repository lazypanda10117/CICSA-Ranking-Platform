from django.shortcuts import reverse
from api import EventAPI, EventActivityAPI, SchoolAPI, TeamAPI
from ....component import CustomElements
from ...base.block.CustomPages import AbstractBasePage


class EventActivityRankingPage(AbstractBasePage):
    def getPagePath(self):
        return 'platform/module/management_ranking/submit_race.html'

    def render(self):
        return super().renderHelper(self.genPageObject())

    def genPageObject(self):
        return dict(
            block_title='Event Activities List',
            action_destination=reverse(
                'panel.module.management_ranking.process_dispatch_param',
                args=['activity ranking', int(self.param["id"])]),
            form_id='event_activity_ranking_form',
            contents=self.genContent())

    def genContent(self):
        def getScoreOptions(school_id):
            options = {**{str(i + 1): dict(selected='', text=str(i + 1)) for i in range(event_team_number)},
                       **{choice: dict(selected='', text=choice) for scoremap_id, choice in
                          CustomElements.Choices().getScoreMapChoices()}}
            options = setDefaultOption(school_id, options)
            return options

        def setDefaultOption(school_id, options):
            try:
                school_result = event_activity_result[str(school_id)]
                options[school_result]['selected'] = 'selected'
            except KeyError:
                print("Result Has Not Been Set Yet.")
            return options

        def getEventSpecificRotation(event_rotation, order, tag):
            return {key: rotation[order - 1] for key, rotation in event_rotation[tag].items()}

        def getEventActivityTeams(event_specific_rotation):
            return list(event_specific_rotation.keys())

        def getEventActivitySchool(event_activity_teams):
            return {school_team_tuple[0]: school_team_tuple[1]
                    for school_team_tuple in [
                        (lambda x: (school_api.getSelf(id=x.team_school), x))
                        (team_api.getSelf(id=event_activity_team_id))
                        for event_activity_team_id in event_activity_teams]}

        def compileContent(event_boat_identifiers, event_activity_schools, event_team_number):
            return {str(i + 1): dict(
                boat_identifier=event_boat_identifiers[i],
                school_name=list(event_activity_schools.keys())[i].school_name,
                event_activity_team=list(event_activity_schools.values())[i].id,
                options=getScoreOptions(list(event_activity_schools.values())[i].id)
            ) for i in range(event_team_number)}

        event_activity_id = int(self.param["id"])
        event_api = EventAPI(self.request)
        event_activity_api = EventActivityAPI(self.request)
        school_api = SchoolAPI(self.request)
        team_api = TeamAPI(self.request)

        event_activity = event_activity_api.getSelf(id=event_activity_id)
        event = event_api.getSelf(id=int(event_activity.event_activity_event_parent))
        event_boat_identifiers = event.event_boat_rotation_name.split(',')
        event_rotation = event.event_rotation_detail
        event_activity_tag = event_activity.event_activity_event_tag
        event_team_number = event.event_team_number
        event_activity_order = event_activity.event_activity_order
        event_activity_result = event_activity.event_activity_result
        event_specific_rotation = getEventSpecificRotation(event_rotation, event_activity_order, event_activity_tag)
        event_activity_teams = getEventActivityTeams(event_specific_rotation)
        event_activity_schools = getEventActivitySchool(event_activity_teams)

        content = compileContent(event_boat_identifiers, event_activity_schools, event_team_number)
        return content

    def parseParams(self, param):
        match = super().parseMatch('\d+')
        param = dict(id=param)
        return param
