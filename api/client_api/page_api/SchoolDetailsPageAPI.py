from django.shortcuts import reverse

from misc.CustomFunctions import UrlFunctions
from misc.CustomFunctions import MiscFunctions
from api.base.GeneralClientAPI import GeneralClientAPI
from api.functional_api import LeagueScoringAPI
from api.model_api import RegionAPI
from api.model_api import SchoolAPI
from api.model_api import SummaryAPI


class SchoolDetailsPageAPI(GeneralClientAPI):
    def __init__(self, request):
        super().__init__(request)
        self.season = self.getSeason()

    def grabPageData(self, **kwargs):
        def getSchoolInfo(school_id):
            school = school_api.getSelf(id=school_id)
            region_api = RegionAPI(self.request)
            region = region_api.getSelf(id=school.school_region)
            season_score = LeagueScoringAPI(self.request, self.season).tryCompileThenCalculateScore(school)
            return dict(
                school_name=school.school_name,
                school_region=(
                    region.region_name, 
                    "{}#{}".format(
                        UrlFunctions.getClientViewLink('schools'), 
                        region.region_name
                    )
                ),
                school_status=school.school_status.capitalize(),
                school_season_score=MiscFunctions.truncateDisplayScore(season_score)
            )

        def getSchoolParticipatedEvents(school_id):
            events = school_api.getParticipatedEvents(school_id, season=self.season)
            school = school_api.getSelf(id=school_id)
            region_api = RegionAPI(self.request)
            region = region_api.getSelf(id=school.school_region)
            summary_api = SummaryAPI(self.request)
            result = []
            for event in events:
                rank = summary_api.getSummaryRankingBySchool(event.id, school_id)
                result.append(dict(
                    name=event.event_name,
                    region=region.region_name,
                    start_date=event.event_start_date,
                    rank=rank,
                    link=reverse('client.view_dispatch_param', args=["event_scoring", event.id]),
                    score=MiscFunctions.truncateDisplayScore(
                        LeagueScoringAPI(self.request).getScoreForEventBySchool(
                            event=event, school=school, compiled=True
                        )
                    )
                ))
            return sorted(result, key=lambda event: event.get('start_date'), reverse=True)

        school_id = kwargs.get("id")
        school_api = SchoolAPI(self.request)

        page_data = dict(
            school_info=getSchoolInfo(school_id),
            school_participated_events=getSchoolParticipatedEvents(school_id)
        )
        return page_data
