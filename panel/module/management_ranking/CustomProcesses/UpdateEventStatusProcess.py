from django.shortcuts import redirect, reverse
from misc.CustomFunctions import AuthFunctions
from api import EventAPI
from ...base.block.CustomProcesses import AbstractBaseProcess


class UpdateEventStatusProcess(AbstractBaseProcess):
    def process(self):
        if AuthFunctions.signed_in(self.request, 'admin'):
            event_api = EventAPI(self.request)
            event_api.updateEventStatus(int(self.param["id"]), self.param["status"])
        return redirect(reverse('panel.module.management_ranking.view_dispatch', args=['event']))

    def parseParams(self, param):
        super().parseMatch('\d+,\w+')
        params = param.split(',')
        param = dict(
            id=params[0],
            status=params[1]
        )
        return param
