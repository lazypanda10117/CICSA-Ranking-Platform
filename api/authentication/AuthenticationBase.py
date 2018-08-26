from cicsa_ranking import models as model
from misc.CustomElements import Dispatcher

class AuthenticationBase():
    def __init__(self, request):
        self.request = request;

    def __getDispatcher(self):
        dispatcher = Dispatcher();
        dispatcher.add(model.EventActivity.__class__.__name__, self.EventActivity);
        dispatcher.add(model.Event.__class__.__name__, self.Event);
        dispatcher.add(model.EventTag.__class__.__name__, self.EventTag);
        dispatcher.add(model.EventTeam.__class__.__name__, self.EventTeam);
        dispatcher.add(model.Log.__class__.__name__, self.Log);
        dispatcher.add(model.Member.__class__.__name__, self.Member);
        dispatcher.add(model.MemberGroup.__class__.__name__, self.MemberGroup);
        dispatcher.add(model.Region.__class__.__name__, self.Region);
        dispatcher.add(model.School.__class__.__name__, self.School);
        dispatcher.add(model.ScoreMapping.__class__.__name__, self.ScoreMapping);
        dispatcher.add(model.Season.__class__.__name__, self.Season);
        dispatcher.add(model.Summary.__class__.__name__, self.Summary);
        dispatcher.add(model.Team.__class__.__name__, self.Team);
        return dispatcher;

    def dispatch(self, key):
        dispatcher = self.__getDispatcher();
        return dispatcher.get(key);