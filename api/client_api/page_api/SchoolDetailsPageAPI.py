from api.base.GeneralClientAPI import GeneralClientAPI

class SchoolDetailsPageAPI(GeneralClientAPI):
    def grabPageData(self, **kwargs):
        def getSchoolInfo(school_id): # or gen?
            return id # temp

        def getSchoolParticipatedEvents(school_id): # or gen?
            return id # temp

        school_id = kwargs.get("id")
        page_data = dict(
            school_info = getSchoolInfo(school_id),
            school_participated_events = getSchoolParticipatedEvents(school_id)
        )
        return page_data