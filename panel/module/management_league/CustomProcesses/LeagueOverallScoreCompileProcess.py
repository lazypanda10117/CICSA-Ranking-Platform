from django.shortcuts import redirect
from django.shortcuts import reverse

from panel.module.base.block.CustomProcesses import AbstractBaseProcess
from api import LeagueScoringAPI


class LeagueOverallScoreCompileProcess(AbstractBaseProcess):
    def process(self):
        post_dict = self.post_data
        LeagueScoringAPI(self.request).computeLeagueScores(
            override=[(school_id, element[0]) for school_id, element in post_dict.items()]
        )
        return redirect(
            reverse(
                'panel.module.management_league.view_dispatch',
                args=['overall']
            )
        )

    def parseParams(self, param):
        super().parseMatch('')
        param = None
        return param
