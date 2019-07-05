from django.views.decorators.csrf import csrf_exempt
from misc.CustomElements import Dispatcher
from panel.module.base.block.Base import AbstractBlockApp
from panel.module.management_league.CustomPages import LeagueSchoolScoreCompilePage
from panel.module.management_league.CustomPages import LeagueOverallScoreCompilePage
from panel.module.management_league.CustomProcesses import LeagueOverallScoreCompileProcess
from panel.module.ModuleRegistry import ModuleRegistry


def index(request):
    return ManagementLeagueView().home(request)


def viewDispatch(request, route, param=''):
    return ManagementLeagueView().viewDispatch(request, route, param)


@csrf_exempt
def processDispatch(request, route, param=''):
    return ManagementLeagueView().processDispatch(request, route, param)


class ManagementLeagueView(AbstractBlockApp.AppView):
    # Block App Base View Inherited Functions
    def getBaseAppName(self):
        return ModuleRegistry.MANAGEMENT_LEAGUE

    def home(self, request):
        return super().index(request, 'panel.module.management_league.view_dispatch', ['overall'])

    def setViewDispatcher(self):
        dispatcher = Dispatcher()
        dispatcher.add('specific', LeagueSchoolScoreCompilePage)
        dispatcher.add('overall', LeagueOverallScoreCompilePage)
        return dispatcher

    def setProcessDispatcher(self):
        dispatcher = Dispatcher()
        dispatcher.add('compile', LeagueOverallScoreCompileProcess)
        return dispatcher
