from django.shortcuts import reverse

from api.base.GeneralClientAPI import GeneralClientAPI
from api.model_api import EventAPI
from api.model_api import EventTypeAPI
from api.model_api import RegionAPI
from api.model_api import SchoolAPI


class RegattasPageAPI(GeneralClientAPI):
    def __init__(self, request):
        super().__init__(request)
        self.season = self.getSeason()

    def grabPageData(self, **kwargs):
        def genEventTable(status):
            status_map = {'future': "Future Events", 'running': "Ongoing Events", 'done': "Completed Events"}
            events = EventAPI(self.request).filterSelf(
                event_status=status, event_season=self.season
            ).order_by('event_start_date')
            event_dict = list(map(lambda event: dict(
                event_name=event.event_name,
                event_link=reverse('client.view_dispatch_param', args=["event_scoring", event.id]),
                event_type=EventTypeAPI(self.request).getSelf(id=event.event_type).event_type_name,
                event_status=status_map[event.event_status] if event.event_status in status_map else event.event_status,
                event_region=RegionAPI(self.request).getSelf(id=event.event_region).region_name,
                event_host=SchoolAPI(self.request).getSelf(id=event.event_host).school_name,
                event_start_date=event.event_start_date.strftime("%B %d, %Y"),
                event_start_date_num=int(event.event_start_date.strftime("%Y%m%d"))
            ), list(events)))
            event_dict = sorted(event_dict, key=(lambda x: x['event_start_date_num']), reverse=True)
            return event_dict
        page_data = dict(
            Ongoing=genEventTable("running"),
            Future=genEventTable("future"),
            Completed=genEventTable("done")
        )
        return page_data


