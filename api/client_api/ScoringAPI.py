from functools import reduce
from misc.CustomFunctions import UrlFunctions
from ..base.GeneralClientAPI import GeneralClientAPI
from ..model_api import EventAPI, EventActivityAPI, SummaryAPI, TeamAPI, EventTypeAPI
from ..model_api import EventTagAPI, RegionAPI, SchoolAPI, SeasonAPI


class ScoringAPI(GeneralClientAPI):
    FLEET_RACE = 1
    TEAM_RACE = 2

    def __getEventDetails(self, event_id):
        return EventAPI(self.request).getSelf(id=event_id)

    def __getEventType(self, event):
        return EventTypeAPI(self.request).getSelf(id=event.event_type).event_type_name

    def __buildEventDetailsDict(self, event):
        result = dict(
            name=event.event_name,
            description=event.event_description,
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
            status=event.event_status,
            start=event.event_start_date.strftime("%Y-%m-%d"),
            end=event.event_end_date.strftime("%Y-%m-%d")
        )
        return result

    def __scoreAdd(self, x, y, team_num):
        def scoreStringMapping(str, team_num):
            # shoud use data from DB later
            if str == "OCF":
                score = team_num + 1
            elif str == "DNF":
                score = team_num + 1
            else:
                score = team_num + 1
            return score

        try:
            value1 = int(x)
        except ValueError:
            value1 = scoreStringMapping(x, team_num)

        try:
            value2 = int(y)
        except ValueError:
            value2 = scoreStringMapping(x, team_num)

        return value1 + value2

    def __buildFleetTable(self, event):
        def __buildFleetScoreTable():
            race_table = dict()
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
                        (lambda x, y: self.__scoreAdd(x, y, event.event_team_number)),
                        race_table[tag][team]["scores"]
                    )
                    race_table[tag][team]["final_score"] = score
            return race_table

        def __buildFleetRankingTable():
            if event.event_status != "done":
                ranking_table = dict()
                for school in schools:
                    ranking_table[school.school_name] = 0
                for tag in event_activity_name_tags:
                    for team in team_ids[tag]:
                        ranking_table[team_school_link[team].school_name] += score_table[tag][team]["final_score"]
                school_ranking_list = [
                    dict(school_name=school_name, score=data, ranking='#', note='')
                    for school_name, data in ranking_table.items()
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
                        else:
                            school_ranking_list[index]['ranking'] = prevRanking
            else:
                summaries = SummaryAPI(self.request).filterSelf(summary_event_parent=event.id)
                school_ranking_list = [
                    dict(
                        school_name=schools.filter(id=summary.summary_event_school).school_name,
                        score=summary.summary_race_score,
                        ranking=  summary.summary_event_ranking + summary.summary_event_override_ranking,
                        note='*' if summary.summary_event_override_ranking != 0 else ''

                    ) for summary in summaries
                ]
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

    def __buildDataTable(self, event):
        if event.event_type == self.FLEET_RACE:
            return self.__buildFleetTable(event)
        elif event.event_type == self.TEAM_RACE:
            pass
        else:
            pass

    def grabPageData(self, **kwargs):
        event_id = kwargs['id']
        event = self.__getEventDetails(event_id)
        event_type = self.__getEventType(event)
        event_details = self.__buildEventDetailsDict(event)
        event_table = self.__buildDataTable(event)
        page_data = dict(
            event_type=event_type,
            event_details=event_details,
            school_current_ranking=event_table['ranking'],
            event_activity_scoring_detail=event_table['score']
        )
        return page_data
