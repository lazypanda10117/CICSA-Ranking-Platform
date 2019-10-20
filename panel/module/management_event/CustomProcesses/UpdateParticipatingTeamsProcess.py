from django.shortcuts import redirect
from django.urls import reverse

from panel.module.base.block.CustomProcesses import AbstractBaseProcess


class UpdateParticipatingTeamsProcess(AbstractBaseProcess):
    def process(self):
        post_dict = dict(self.request.POST)
        print(post_dict)
        return redirect(
            reverse(
                'panel.module.management_event.view_dispatch_param',
                args=['team', self.param['id']]
            )
        )

    def parseParams(self, param):
        super().parseMatch('\d+')
        param = dict(id=param)
        return param
