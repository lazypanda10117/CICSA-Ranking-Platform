from functools import reduce
from misc.CustomFunctions import UrlFunctions
from ..base import GeneralClientAPI
from ..model_api import EventAPI, EventActivityAPI, SummaryAPI, TeamAPI, EventTeamAPI, EventTypeAPI
from ..model_api import EventTagAPI, RegionAPI, SchoolAPI, SeasonAPI


class ScoringAPI(GeneralClientAPI):
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
            start=event.event_start_date,
            end=event.event_end_date
        )
        return result

    def __scoreAdd(self, x, y, race_num):
        def scoreStringMapping(str, race_num):
            if str == "OCF":
                score = race_num + 1
            elif str == "DNF":
                score = race_num + 1
            else:
                score = race_num + 1
            return score

        try:
            value1 = int(x)
        except ValueError:
            value1 = scoreStringMapping(x, race_num)

        try:
            value2 = int(y)
        except ValueError:
            value2 = scoreStringMapping(x, race_num)

        return value1 + value2

    def __buildFleetTable(self, event):
        def __buildFleetScoreTable():
            race_table = dict()
            for tag in event_activity_tags:
                race_table[tag] = dict()
                restricted_eas = event_activities.filter(event_activity_event_tag=tag).order_by('event_activity_order')
                for ea in restricted_eas:
                    result = ea.event_activity_result
                    if bool(result):
                        for team, rank in result.items():
                            team_name = team_name_link[team]
                            if race_table[tag][team] is None:
                                race_table[tag][team] = dict(team_name=team_name, scores=list(), final_score=0)
                            race_table[tag][team]["scores"].append(rank)
                    else:
                        for teams in team_ids[tag]:
                            for team in teams:
                                team_name = team_name_link[team]
                                if race_table[tag][team] is None:
                                    race_table[tag][team] = dict(team_name=team_name, scores=list(), final_score=0)
                                race_table[tag][team]["scores"].append(0)
            for tag in event_activity_tags:
                for team in team_ids[tag]:
                    score = reduce(
                        (lambda x, y: self.__scoreAdd(x, y, event.race_number)),
                        race_table[tag][team]["scores"]
                    )
                    race_table[tag][team]["final_score"] = score
            return race_table

        def __buildFleetRankingTable():
            if event.event_status == "done":
                ranking_table = dict()
                for school in schools:
                    ranking_table[school.school_name] = 0
                for tag in event_activity_tags:
                    for team in team_ids[tag]:
                        ranking_table[team_school_link[team].school_name] += ranking_table[tag][team]["final_score"]
                school_ranking_list = [
                    dict(school_name=school_name, score=data, ranking='#', note='')
                    for school_name, data in ranking_table
                ]
                sorted(school_ranking_list, key=(lambda x: x['score']))
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
        schools = SchoolAPI(self.requset).filterSelf(id=list(map(lambda x: int(x), event.event_school_ids)))
        event_activity_tags = list()
        team_ids = dict()
        team_flatten_ids = list()
        team_school_link = dict()
        team_name_link = dict()
        distinct_eas = event_activities.distinct('event_activity_event_tag')
        for ea in distinct_eas:
            event_activity_tags += EventTagAPI(self.request).getSelf(id=ea.event_activity_event_tag).event_tag_name
            team_flatten_ids += ea.event_activity_result.keys()
            team_ids[ea.event_activity_event_tag] = ea.event_activity_result.keys()
        for team in TeamAPI(self.request).filterSelf(id__in=team_ids):
            team_school_link[team.id] = schools.filter(id=team.team_school)
            team_name_link[team.id] = team_school_link[team.id].school_name + team.team_name

        rank_table = __buildFleetRankingTable()
        score_table = __buildFleetScoreTable()
        return dict(ranking=rank_table, score=score_table)

    def __buildDataTable(self, event):
        if event.event_type == "fleet":
            return self.__buildFleetTable(event)
        elif event.event_type == "team":
            pass

    def __compileScoring(self, event_id):
        # check status: if ongoing then use event activity, if ended, the use summary.
        pass

    def getPageData(self, **kwargs):
        event_id = kwargs['event_id']
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
