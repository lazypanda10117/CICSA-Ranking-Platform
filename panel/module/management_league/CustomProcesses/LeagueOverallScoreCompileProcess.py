from django.shortcuts import redirect, reverse

from misc.CustomFunctions import RequestFunctions
from api.model_api import ConfigAPI
from api.functional_api import LeagueScoringAPI
from panel.module.base.block.CustomProcesses import AbstractBaseProcess


class LeagueOverallScoreCompileProcess(AbstractBaseProcess):
    def process(self):
        post_dict = dict(self.request.POST)
        current_configuration = ConfigAPI(self.request).getConfig()
        current_season = current_configuration.config_current_season
        # update the db according to override values, otherwise, compute the calculated values again
        return redirect(
            reverse(
                'panel.module.management_league.view_dispatch',
                args=['overall']
            )
        )

    def parseParams(self, param):
        super().parseMatch('')
        return None
