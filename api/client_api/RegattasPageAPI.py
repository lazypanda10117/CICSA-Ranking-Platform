from django.shortcuts import reverse
from ..base.GeneralClientAPI import GeneralClientAPI
from ..model_api import EventAPI, EventTypeAPI, RegionAPI, SchoolAPI


class RegattasPageAPI(GeneralClientAPI):
    def grabPageData(self, **kwargs):
        def genEventTable(status):
            events = EventAPI(self.request).filterSelf(event_status=status).order_by('event_start_date')
            event_dict = list(map(lambda event: dict(
                event_name=event.event_name,
                event_link=reverse('client.scoring', args=[event.id]),
                event_type=EventTypeAPI(self.request).getSelf(id=event.event_type).event_type_name,
                event_status=event.event_status,
                event_region=RegionAPI(self.request).getSelf(id=event.event_region).region_name,
                event_host=SchoolAPI(self.request).getSelf(id=event.event_host).school_name,
                event_start_date=event.event_start_date.strftime("%B %d, %Y")
            ), list(events)))
            event_dict = sorted(event_dict, key=(lambda x: x['event_start_date']))
            return event_dict
        page_data = dict(
            Running=genEventTable("running"),
            Future=genEventTable("future"),
            Done=genEventTable("done")
        )
        return page_data


