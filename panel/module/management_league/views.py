from django.views.decorators.csrf import csrf_exempt
from misc.CustomElements import Dispatcher
from ..base.block.Base import AbstractBlockApp
from .CustomPages import LeagueRankingPage, LeagueScoreCompilePage
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
        return super().index(request, 'panel.module.management_league.view_dispatch', ['ranking'])

    def setViewDispatcher(self):
        dispatcher = Dispatcher()
        dispatcher.add('ranking', LeagueRankingPage)
        dispatcher.add('compile', LeagueScoreCompilePage)
        return dispatcher

    def setProcessDispatcher(self):
        dispatcher = Dispatcher()
        return dispatcher
