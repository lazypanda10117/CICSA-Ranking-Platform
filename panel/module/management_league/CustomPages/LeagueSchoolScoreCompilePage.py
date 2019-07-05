from django.shortcuts import reverse

from cicsa_ranking.models import Event
from misc.CustomFunctions import MiscFunctions
from api import ConfigAPI
from api import EventAPI
from api import SchoolAPI
from api import SummaryAPI
from api import LeagueScoringAPI
from panel.module.base.block.CustomPages import AbstractBasePage


class LeagueSchoolScoreCompilePage(AbstractBasePage):
    def getPagePath(self):
        return 'platform/module/management_league/specific_score.html'

    def render(self):
        return super().renderHelper(self.genPageObject())

    def genPageObject(self):
        return dict(
            block_title='Specific School Score View for {}'.format(
                SchoolAPI(self.request).getSelf(id=self.param.get("school_id")).school_name
            ),
            redirection_destination=reverse(
                'panel.module.management_league.view_dispatch',
                args=['overall']),
            contents=self.genContent()
        )

    def __eventUrlTransformer(self, event_id):
        return reverse(
            'client.view_dispatch_param',
            args=['scoring', event_id]
        )

    def __checkIsScoreUsed(self, event, score_list, final_events, average_factor):
        for final_event in final_events:
            if event.id == final_event.id:
                return True

        for idx, score_event in enumerate(score_list):
            loop_event = score_event[1]
            if idx < average_factor:
                if event.id == loop_event.id:
                    return True
            else:
                break

        return False

    def genContent(self):
        content = list()
        # TODO: Remove these current season stuff as it will be handled by ModelAPI
        current_season = ConfigAPI(self.request).getConfig().config_current_season
        school_id = self.param.get("school_id")
        school = SchoolAPI(self.request).getSelf(id=school_id)
        participated_events = SchoolAPI(self.request).getParticipatedEvents(
            school_id,
            Event.EVENT_STATUS_DONE,
            current_season
        )
        rankingMap = SummaryAPI(self.request).getAllSummaryRankingBySchool(school_id)
        league_scoring_api = LeagueScoringAPI(self.request)
        average_events = list(filter(lambda event: event.event_name not in Event.EVENT_NAME_FINAL_RACE, participated_events))
        final_events = list(filter(lambda event: event.event_name in Event.EVENT_NAME_FINAL_RACE, participated_events))
        average_factor = league_scoring_api.getAverageFactor(
                                school.school_region,
                                len(average_events)
                            )
        sorted_score_list = league_scoring_api.getReverseSortedEventScoresList(
                                school, 
                                average_events
                            )
        for event in participated_events:
            score = league_scoring_api.getScoreForEventBySchool(event, school, False)
            content.append(
                dict(
                    event_id=event.id,
                    event_name=event.event_name,
                    event_url=self.__eventUrlTransformer(event.id),
                    event_date=event.event_start_date,
                    school_summary_ranking=rankingMap.get(event.id),
                    school_summary_score=MiscFunctions.truncateDisplayScore(score),
                    used_score_in_calculation=self.__checkIsScoreUsed(
                        event,
                        sorted_score_list,
                        final_events,
                        average_factor
                    ),
                )
            )
        content_list = sorted(content, key=lambda x: x.get('event_date'))
        return content_list

    def parseParams(self, param):
        super().parseMatch('\d+')
        param = dict(school_id=param)
        return param
