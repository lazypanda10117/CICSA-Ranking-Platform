from django.shortcuts import reverse
from api.base.GeneralClientAPI import GeneralClientAPI
from api.model_api import EventAPI, EventTypeAPI, RegionAPI, SchoolAPI


class SchoolsPageAPI(GeneralClientAPI):
    def grabPageData(self, **kwargs):
        def genSchoolTable(region):
            schools = SchoolAPI(self.request).filterSelf(school_region=region).order_by('school_name')
            school_dict = list(map(lambda school: dict(
                school_name=school.school_name,
                school_team_name=school.school_default_team_name,
                school_status=school.school_status,
                school_season_score=school.school_season_score,
                school_link='#'
            ), list(schools)))
            return school_dict

        page_data = dict()
        regions = RegionAPI(self.request).excludeSelf(region_name="Other").order_by('region_name')
        for region in regions:
            region_name = region.region_name
            page_data[region_name] = genSchoolTable(region.id)
        return page_data
