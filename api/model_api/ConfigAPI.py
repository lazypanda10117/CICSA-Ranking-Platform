from cicsa_ranking.models import Config
from api.base.GeneralModelAPI import GeneralModelAPI
from api.model_api.AccountAPI import AccountAPI


class ConfigAPI(GeneralModelAPI):
    @staticmethod
    def getBaseClass():
        return Config

    def getConfig(self):
        return self.getAll()[0]

    def getSeason(self):
        return self.getConfig().config_current_season
