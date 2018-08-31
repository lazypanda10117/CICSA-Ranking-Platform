from misc.CustomElements import Dispatcher
from ...config.team.management_data.CustomPages import *
from ...config.team.management_data.CustomForms import *


class AuthenticationTeam:
    @staticmethod
    def getIdentifier():
        return 'team'

    class ManagementData:
        @staticmethod
        def getTemplateBase():
            return 'platform/module/management_data/team_base.html'
