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

    def __buildFleetRaceTable(self, event_id):

    def __buildActivityTable(self, event_type, event_id):
        if(event_type == )


    def __compileScoring(self, event_id):
        # check status: if ongoing then use event activity, if ended, the use summary.
        pass

    def getPageData(self, **kwargs):
        event_id = kwargs['event_id']
        event_details = self.__getEventDetails(event_id)
        event_type = self.__getEventType(event_details)
        page_data = dict(
            event_type = dict(),
            event_details=dict(),  # text : link
            school_current_ranking=dict(),  # calculate from getting from event activity
            event_activity_scoring_detail=dict()  # event tag 1: detail(event activities ... ) event tag 2: detail()
            # dont count if score is empty json and check so dont display error
            # also remember to sort by order
        )
        return page_data
