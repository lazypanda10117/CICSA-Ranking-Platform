from cicsa_ranking import models as model
from .AuthenticationBase import AuthenticationBase
from .AuthenticantionComponentBase import AuthenticationComponentBase


class AuthenticationAdmin(AuthenticationBase):
    class EventActivity(AuthenticationComponentBase):
        def setBaseModelClass(self):
            return model.EventActivity;

    class Event(AuthenticationComponentBase):
        def setBaseModelClass(self):
            return model.Event;

    class EventTag(AuthenticationComponentBase):
        def setBaseModelClass(self):
            return model.EventTag;

    class EventTeam(AuthenticationComponentBase):
        def setBaseModelClass(self):
            return model.EventTeam;

    class Log(AuthenticationComponentBase):
        def setBaseModelClass(self):
            return model.Log;

    class Member(AuthenticationComponentBase):
        def setBaseModelClass(self):
            return model.Member;

    class MemberGroup(AuthenticationComponentBase):
        def setBaseModelClass(self):
            return model.MemberGroup;

    class Region(AuthenticationComponentBase):
        def setBaseModelClass(self):
            return model.Region;

    class School(AuthenticationComponentBase):
        def setBaseModelClass(self):
            return model.School;

    class ScoreMapping(AuthenticationComponentBase):
        def setBaseModelClass(self):
            return model.ScoreMapping;

    class Season(AuthenticationComponentBase):
        def setBaseModelClass(self):
            return model.Season;

    class Summary(AuthenticationComponentBase):
        def setBaseModelClass(self):
            return model.Summary;

    class Team(AuthenticationComponentBase):
        def setBaseModelClass(self):
            return model.Team;