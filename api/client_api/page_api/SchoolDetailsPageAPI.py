from django.shortcuts import reverse
from api.base.GeneralClientAPI import GeneralClientAPI
from api.model_api import ConfigAPI, RegionAPI, SchoolAPI, ScoreAPI, SummaryAPI

class SchoolDetailsPageAPI(GeneralClientAPI):
    def grabPageData(self, **kwargs):
        def getSchoolInfo(school_id, season_id):
            # name region status season_score
            school = school_api.getSelf(id=school_id)
            region_api = RegionAPI(self.request)
            region = region_api.getSelf(id=school.school_region)
            score_api = ScoreAPI(self.request)
            season_score = score_api.getSeasonScoreValue(school_id, season_id)
            return dict(
                school_name=school.school_name,
                school_region=region.region_name,
                school_status=school.school_status,
                school_season_score=(season_score if season_score != -1 else "-")
            )

        def getSchoolParticipatedEvents(school_id, season_id):
            events = school_api.getParticipatedEvents(school_id, season=season_id)
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
                    link=reverse('client.view_dispatch_param', args=["scoring", event.id]),
                ))
            return result

        school_id = kwargs.get("id")
        school_api = SchoolAPI(self.request)

        current_configuration = ConfigAPI(self.request).getAll()[0]
        current_season = current_configuration.config_current_season

        page_data = dict(
            school_info=getSchoolInfo(school_id, current_season),
            school_participated_events=getSchoolParticipatedEvents(school_id, current_season)
        )
        return page_data