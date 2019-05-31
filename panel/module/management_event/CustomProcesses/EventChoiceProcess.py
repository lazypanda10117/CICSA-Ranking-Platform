from django.shortcuts import redirect, reverse
from ...base.block.CustomProcesses import AbstractBaseProcess


class EventChoiceProcess(AbstractBaseProcess):
    def process(self):
        return redirect(
            reverse(
                'blackbox.block_app.management_event.view_dispatch',
                args=['event', self.param["type"]])
        )

    def parseParams(self, param):
        super().parseMatch('\w+')
        param = dict(type=param)
        return param
