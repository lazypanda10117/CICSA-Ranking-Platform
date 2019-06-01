from api.model_api import *
from misc.CustomElements import Dispatcher
from misc.CustomFunctions import MiscFunctions


def getAllModelAPIs():
    return [
        AccountAPI,
        ConfigAPI,
        EventActivityAPI,
        EventAPI,
        EventTagAPI,
        EventTeamAPI,
        EventTypeAPI,
        LogAPI,
        MemberAPI,
        MemberGroupAPI,
        NewsBumpAPI,
        NewsCommentAPI,
        NewsPostAPI,
        RegionAPI,
        SchoolAPI,
        ScoreMappingAPI,
        SeasonAPI,
        SummaryAPI,
        TeamAPI
    ]


def getModelAPIDispatcher():
    dispatcher = Dispatcher()
    for api in getAllModelAPIs():
        dispatcher.add(api.getBaseClass().__name__, api)
    return dispatcher


def applyModelAPI(model, request):
    return getModelAPIDispatcher().get(MiscFunctions.getModelName(model))(request)
