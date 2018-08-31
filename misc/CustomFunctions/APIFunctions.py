from api.model_api import *
from misc.CustomElements import Dispatcher


def getAllModelAPIs():
    return [
        EventActivityAPI,
        EventAPI,
        EventTagAPI,
        EventTeamAPI,
        EventTypeAPI,
        LogAPI,
        MemberAPI,
        MemberGroupAPI,
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
        dispatcher.add(api().class_name, api)
    return dispatcher
