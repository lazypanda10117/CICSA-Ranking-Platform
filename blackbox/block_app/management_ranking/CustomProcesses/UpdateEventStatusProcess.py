from django.shortcuts import redirect, reverse
from misc.GeneralFunctions import generalFunctions as gf
from blackbox import api
from blackbox.block_app.base.CustomProcesses import AbstractBaseProcess

class UpdateEventStatusProcess(AbstractBaseProcess):
    def process(self):
        if gf.signed_in(self.request, 'admin'):
            event_api = api.EventAPI(self.request);
            event_api.updateEventStatus(int(self.param["id"]), self.param["status"]);
        return redirect(reverse('blackbox.block_app.management_ranking.view_dispatch', args=['event']));

    def parseParams(self, param):
        match = super().parseMatch('\d+/\s+');
        params = param.split('/');
        param = dict(
            id=params[0],
            status=params[1]
        );
        return param;


