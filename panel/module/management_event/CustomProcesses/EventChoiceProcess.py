from django.shortcuts import redirect, reverse
from blackbox.block_app.base.CustomProcesses import AbstractBaseProcess

class EventChoiceProcess(AbstractBaseProcess):
    def process(self):
        return redirect(
            reverse(
                'blackbox.block_app.management_event.view_dispatch',
                args=['event', self.param["type"]])
        );

    def parseParams(self, param):
        match = super().parseMatch('\s+');
        param = dict(type=param);
        return param;