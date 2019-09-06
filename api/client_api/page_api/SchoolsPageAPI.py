from django.shortcuts import reverse

from cicsa_ranking.models import Region
from misc.CustomFunctions import MiscFunctions
from api.base.GeneralClientAPI import GeneralClientAPI
from api.functional_api import LeagueScoringAPI
from api.model_api import RegionAPI
from api.model_api import SchoolAPI


class SchoolsPageAPI(GeneralClientAPI):
    def grabPageData(self, **kwargs):
        def genSchoolTable(region):
            schools = SchoolAPI(self.request).filterSelf(school_region=region).order_by('school_name')
            school_dict = list(map(lambda school: dict(
                school_name=school.school_name,
                school_team_name=school.school_default_team_name,
                school_status=school.school_status,
                school_season_score=MiscFunctions.truncateDisplayScore(
                    LeagueScoringAPI(self.request).tryCompileThenCalculateScore(school)
                ),
                school_link=reverse('client.view_dispatch_param', args=["school_specific", school.id])
            ), list(schools)))
            return school_dict

        page_data = dict()
        regions = RegionAPI(self.request).excludeSelf(
            region_name__in=Region.REGION_EXCLUDED_NAMES
        ).order_by('region_name')
        for region in regions:
            region_name = region.region_name
            page_data[region_name] = genSchoolTable(region.id)
        return page_data
