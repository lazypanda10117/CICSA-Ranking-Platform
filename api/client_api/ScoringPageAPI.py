import re
from functools import reduce
from django.shortcuts import reverse
from misc.CustomFunctions import UrlFunctions, MiscFunctions
from misc.CustomElements import EquationParser
from ..base.GeneralClientAPI import GeneralClientAPI
from ..model_api import EventAPI, EventActivityAPI, SummaryAPI, TeamAPI, EventTypeAPI
from ..model_api import EventTagAPI, RegionAPI, SchoolAPI, SeasonAPI, ScoreMappingAPI


class ScoringPageAPI(GeneralClientAPI):
    FLEET_RACE = 'fleet race'
    TEAM_RACE = 'team race'

    def getEventDetails(self, event_id):
        return EventAPI(self.request).getSelf(id=event_id)

    def __getEventType(self, event):
        return EventTypeAPI(self.request).getSelf(id=event.event_type).event_type_name

    def buildEventDetailsDict(self, event):
        status_map = {'future': "Future Regattas", 'running': "Ongoing Regattas", 'done': "Completed Regattas"}
        result = dict(
            name=event.event_name,
            description=event.event_description,
            scoring=('Scoring Page', reverse('client.scoring', args=[event.id])),
            rotation=('Rotation Page', reverse('client.rotation', args=[event.id])),
            season=(
                SeasonAPI(self.request).getSelf(id=event.event_season).season_name,
                UrlFunctions.getClientViewLink('season', event.event_season)
            ),
            region=(
                RegionAPI(self.request).getSelf(id=event.event_region).region_name,
                UrlFunctions.getClientViewLink('region', event.event_region)
            ),
            host=(
                SchoolAPI(self.request).getSelf(id=event.event_host).school_name,
                UrlFunctions.getClientViewLink('host', event.event_host)
            ),
            location=event.event_location,
            status=status_map[event.event_status],
            start=event.event_start_date.strftime("%Y-%m-%d"),
            end=event.event_end_date.strftime("%Y-%m-%d")
        )
        return result

    def __compileScoreMap(self, event):
        def eqtParser(equation_string):
            replace_dict = dict(RACE=event.event_race_number, TEAM=event.event_team_number)
            arithmetic_exp = MiscFunctions.simpleEqtFormatter(equation_string, replace_dict)
            try:
                result = int(EquationParser().eval(arithmetic_exp))
            except:
                result = replace_dict['RACE'] + 1
            return result

        def scoreStringMapping():
            score_mappings = ScoreMappingAPI(self.request).filterSelf()
            score_name_map = {score_map.score_name: score_map.score_value for score_map in score_mappings}
            return {score_name: eqtParser(score_eqt) for score_name, score_eqt in score_name_map.items()}

        return scoreStringMapping()

    def __scoreAdd(self, x, y, score_map):
        reg = re.compile("[ ]\(\d+\)$")
        try:
            value1 = int(x)
        except ValueError:
            x = x[:reg.search(x).span()[0]]
            value1 = score_map[x]
        try:
            value2 = int(y)
        except ValueError:
            y= y[:reg.search(y).span()[0]]
            value2 = score_map[y]
        return value1 + value2

    def __buildFleetTable(self, event):
        def __buildFleetScoreTable():
            race_table = dict()
            event_score_map = self.__compileScoreMap(event)
            for tag_id, tag in zip(event_activity_id_tags, event_activity_name_tags):
                race_table[tag] = dict()
                restricted_eas = event_activities.filter(
                    event_activity_event_tag=tag_id
                ).order_by('event_activity_order')
                for ea in restricted_eas:
                    result = ea.event_activity_result
                    if bool(result):
                        for team, rank in result.items():
                            team_id = int(team)
                            team_name = team_name_link[team_id]
                            rank = rank if rank not in event_score_map else rank + ' (' + str(event_score_map[rank]) + ')'
                            if team_id not in race_table[tag]:
                                race_table[tag][team_id] = dict(team_name=team_name, scores=list(), final_score=0)
                            race_table[tag][team_id]["scores"].append(rank)
                    else:
                        for team in team_ids[tag]:
                            team_name = team_name_link[team]
                            if team not in race_table[tag]:
                                race_table[tag][team] = dict(team_name=team_name, scores=list(), final_score=0)
                            race_table[tag][team]["scores"].append(0)

            for tag in event_activity_name_tags:
                for team in team_ids[tag]:
                    score = reduce(
                        (lambda x, y: self.__scoreAdd(x, y, event_score_map)),
                        race_table[tag][team]["scores"]
                    )
                    race_table[tag][team]["final_score"] = score

            for tag in event_activity_name_tags:
                temp_table = sorted(race_table[tag].items(), key=lambda x: x[1]["final_score"])
                race_table[tag] = {data[0]: data[1] for data in temp_table}

            for tag in event_activity_name_tags:
                prevRanking = 1
                prevScore = 0
                for index, team in enumerate(race_table[tag]):
                    if race_table[tag][team]["final_score"] == 0:
                        race_table[tag][team]["rank"] = '#'
                    else:
                        if race_table[tag][team]["final_score"] > prevScore:
                             prevRanking = index + 1
                             prevScore = race_table[tag][team]["final_score"]
                        race_table[tag][team]["rank"] = prevRanking

            return race_table

        def __buildFleetRankingTable():
            if event.event_status != "done":
                ranking_table = dict()
                for school in schools:
                    ranking_table[school.id] = 0
                for tag in event_activity_name_tags:
                    for team in team_ids[tag]:
                        ranking_table[team_school_link[team].id] += score_table[tag][team]["final_score"]
                school_ranking_list = [
                    dict(
                        school_id=school_id,
                        school_name=schools.get(id=school_id).school_name,
                        score=data,
                        ranking='#',
                        base_ranking='#',
                        override_ranking=0,
                        need_override=False,
                        note='-'
                    ) for school_id, data in ranking_table.items()
                ]
                school_ranking_list = sorted(school_ranking_list, key=(lambda x: x['score']))
                prevRanking = 1
                prevScore = 0
                for index, school_ranking_data in enumerate(school_ranking_list):
                    if school_ranking_data['score'] != 0:
                        if school_ranking_data['score'] > prevScore:
                            prevRanking = index + 1
                            prevScore = school_ranking_data['score']
                        school_ranking_list[index]['ranking'] = prevRanking
                        school_ranking_list[index]['base_ranking'] = prevRanking
            else:
                summaries = list(SummaryAPI(self.request).filterSelf(summary_event_parent=event.id))
                school_ranking_list = [
                    dict(
                        school_id=summary.summary_event_school,
                        school_name=schools.get(id=summary.summary_event_school).school_name,
                        score=summary.summary_event_race_score,
                        ranking=summary.summary_event_ranking + summary.summary_event_override_ranking,
                        base_ranking=summary.summary_event_ranking,
                        override_ranking=summary.summary_event_override_ranking,
                        need_override=True if summary.summary_event_override_ranking != 0 else False,
                        note='Tie-breaker' if summary.summary_event_override_ranking != 0 else '-'
                    ) for index, summary in enumerate(summaries)
                ]
            school_ranking_list = sorted(school_ranking_list, key=(lambda x: x['ranking']))
            # loop to check if entry needs override
            for index, school_ranking_data in enumerate(school_ranking_list):
                duplicates = sum(
                    (1 if result['base_ranking'] == school_ranking_data['base_ranking'] else 0) for result in
                    school_ranking_list)
                if duplicates > 1:
                    school_ranking_list[index]['need_override'] = True
            return school_ranking_list

        event_activities = EventActivityAPI(self.request).filterSelf(event_activity_event_parent=event.id)
        schools = SchoolAPI(self.request).filterSelf(id__in=list(map(lambda x: int(x), event.event_school_ids)))
        teams = EventAPI(self.request).getEventCascadeTeams(event.id)
        event_activity_id_tags = list()
        event_activity_name_tags = list()
        team_ids = dict()
        team_school_link = dict()
        team_name_link = dict()
        distinct_eas = event_activities.distinct('event_activity_event_tag')
        team_flatten_ids = [team.id for team in teams]
        for ea in distinct_eas:
            event_tag_name = EventTagAPI(self.request).getSelf(id=ea.event_activity_event_tag).event_tag_name
            event_activity_name_tags.append(event_tag_name)
            event_activity_id_tags.append(ea.event_activity_event_tag)
            team_ids[event_tag_name] = [team.id for team in teams.filter(team_tag_id=ea.event_activity_event_tag)]
        for team in TeamAPI(self.request).filterSelf(id__in=team_flatten_ids):
            team_school_link[team.id] = schools.get(id=team.team_school)
            team_name_link[team.id] = team_school_link[team.id].school_name + ' - ' + team.team_name

        score_table = __buildFleetScoreTable()
        rank_table = __buildFleetRankingTable()
        return dict(ranking=rank_table, score=score_table)

    def buildDataTable(self, event):
        event_type_name = EventTypeAPI(self.request).getSelf(id=event.event_type).event_type_name
        if event_type_name == self.FLEET_RACE:
            return self.__buildFleetTable(event)
        elif event_type_name == self.TEAM_RACE:
            pass
        else:
            pass

    def grabPageData(self, **kwargs):
        event_id = kwargs['id']
        event = self.getEventDetails(event_id)
        event_type = self.__getEventType(event)
        event_details = self.buildEventDetailsDict(event)
        event_table = self.buildDataTable(event)
        page_data = dict(
            event_type=event_type,
            event_details=event_details,
            school_current_ranking=event_table['ranking'],
            event_activity_scoring_detail=event_table['score']
        )
        return page_data
