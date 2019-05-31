from django.shortcuts import reverse
from api.base.GeneralClientAPI import GeneralClientAPI
from api.model_api import ConfigAPI, RegionAPI, SchoolAPI

class SchoolDetailsPageAPI(GeneralClientAPI):
    def grabPageData(self, **kwargs):
        def getSchoolInfo(school_id): # or gen?
            # name region status season_score
            school = school_api.getSelf(id=school_id)
            region_api = RegionAPI(self.request)
            region = region_api.getSelf(id=school.school_region)
            return dict(
                school_name=school.school_name,
                school_region=region.region_name,
                school_status=school.school_status,
                school_season_score="Twice" # TODO
            )

        def getSchoolParticipatedEvents(school_id, season): # or gen?
            events = school_api.getParticipatedEvents(school_id, season=season)
            school = school_api.getSelf(id=school_id)
            region_api = RegionAPI(self.request)
            region = region_api.getSelf(id=school.school_region)
            rank = "Twice"
            link = "https://channels.vlive.tv/EDBF/home"
            return [dict(
                name=event.event_name,
                region=region.region_name,
                start_date=event.event_start_date,
                rank=rank,
                link=reverse('client.view_dispatch_param', args=["scoring", event.id]),
            ) for event in events]

        school_id = kwargs.get("id")
        school_api = SchoolAPI(self.request)

        current_configuration = ConfigAPI(self.request).getAll()[0]
        current_season = current_configuration.config_current_season

        page_data = dict(
            school_info=getSchoolInfo(school_id),
            school_participated_events=getSchoolParticipatedEvents(school_id, current_season)
        )
        return page_data