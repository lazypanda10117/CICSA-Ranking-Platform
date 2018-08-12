from django.shortcuts import reverse
from blackbox import api
from blackbox.block_app.base.CustomPages import AbstractBasePage
from blackbox.block_app.base.CustomComponents import BlockObject, BlockSet, PageObject
class EventActivityRankingPage():

    def specificEvent(request, event_id):
        return kickRequest(request, True, render(
            request, 'ranking_management/displayList.html',
            {'title': 'Event Activities List', 'event_activity_list': genEventActivityList(request, event_id)}));
        pass;

    def specificEventActivity(request, event_activity_id):

        def getScoreOptions(school_id):
            options = {**{str(i + 1): dict(selected='', text=str(i + 1)) for i in range(event_team_number)},
                       **{choice: dict(selected='', text=choice) for scoremap_id, choice in
                          Choices().getScoreMapChoices()}};
            options = setDefaultOption(school_id, options);
            return options;

        def setDefaultOption(school_id, options):
            try:
                school_result = event_activity_result[str(school_id)];
                options[school_result]['selected'] = 'selected';
            except KeyError:
                print("Result Has Not Been Set Yet.")
            return options;

        event_api = EventAPI(request);
        event_activity_api = EventActivityAPI(request);
        event_activity = event_activity_api.getEventActivity(id=int(event_activity_id));
        event = event_api.getEvent(id=int(event_activity.event_activity_event_parent));
        event_boat_identifiers = event.event_boat_rotation_name.split(',');
        event_rotation = event.event_rotation_detail;
        event_activity_tag = event_activity.event_activity_event_tag;
        event_team_number = event.event_team_number;
        event_activity_order = event_activity.event_activity_order;
        event_activity_result = event_activity.event_activity_result;
        event_specific_rotation = {key: rotation[event_activity_order - 1]
                                   for key, rotation in event_rotation[str(event_activity_tag)].items()};
        event_activity_teams = list(event_specific_rotation.keys());
        event_activity_schools = {school_team_tuple[0]: school_team_tuple[1]
                                  for school_team_tuple in [
                                      (lambda x: (getModelObject(School, id=x.team_school), x))
                                      (getModelObject(Team, id=event_activity_team_id))
                                      for event_activity_team_id in event_activity_teams]};

        contents = {str(i + 1): dict(
            boat_identifier=event_boat_identifiers[i],
            school_name=list(event_activity_schools.keys())[i].school_name,
            event_activity_team=list(event_activity_schools.values())[i].id,
            options=getScoreOptions(list(event_activity_schools.values())[i].id)
        ) for i in range(event_team_number)}
        return kickRequest(request, True, render(
            request, 'ranking_management/eventActivityRace.html',
            {'block_title': 'Event Activity Ranking',
             'action_destination': reverse('blackbox.block_app.management_ranking.process_dispatch_param', args=['', event_activity.id]),
             'form_id': "event_activity_ranking_form",
             'contents': contents}));