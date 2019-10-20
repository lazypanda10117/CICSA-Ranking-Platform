from abc import abstractmethod
from cicsa_ranking import models as model
from misc.CustomElements import Dispatcher


class AuthenticationBase:
    def __init__(self, request):
        self.request = request

    @abstractmethod
    def getAuthenticationType(self):
        pass

    def __getDispatcher(self):
        dispatcher = Dispatcher()
        dispatcher.add(model.Account.__name__, self.Account)
        dispatcher.add(model.Config.__name__, self.Config)
        dispatcher.add(model.NewsPost.__name__, self.NewsPost)
        dispatcher.add(model.NewsComment.__name__, self.NewsComment)
        dispatcher.add(model.NewsBump.__name__, self.NewsBump)
        dispatcher.add(model.EventType.__name__, self.EventType)
        dispatcher.add(model.SchoolTeam.__name__, self.SchoolTeam)
        dispatcher.add(model.Score.__name__, self.Score)
        dispatcher.add(model.EventActivity.__name__, self.EventActivity)
        dispatcher.add(model.Event.__name__, self.Event)
        dispatcher.add(model.EventTag.__name__, self.EventTag)
        dispatcher.add(model.EventTeam.__name__, self.EventTeam)
        dispatcher.add(model.Log.__name__, self.Log)
        dispatcher.add(model.Member.__name__, self.Member)
        dispatcher.add(model.MemberGroup.__name__, self.MemberGroup)
        dispatcher.add(model.Region.__name__, self.Region)
        dispatcher.add(model.School.__name__, self.School)
        dispatcher.add(model.ScoreMapping.__name__, self.ScoreMapping)
        dispatcher.add(model.Season.__name__, self.Season)
        dispatcher.add(model.Summary.__name__, self.Summary)
        dispatcher.add(model.Team.__name__, self.Team)
        return dispatcher

    def dispatch(self, key):
        dispatcher = self.__getDispatcher()
        return dispatcher.get(key)
