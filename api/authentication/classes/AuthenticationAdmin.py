from cicsa_ranking import models as model
from api.authentication import AuthenticationType
from api.authentication.base.AuthenticationBase import AuthenticationBase
from api.authentication.base.AuthenticationComponentBase import AuthenticationComponentBase


class AuthenticationAdmin(AuthenticationBase):

    def getAuthenticationType(self):
        return AuthenticationType.ADMIN

    class Account(AuthenticationComponentBase):
        def setBaseModelClass(self):
            return model.Account

    class NewsPost(AuthenticationComponentBase):
        def setBaseModelClass(self):
            return model.NewsPost

    class NewsComment(AuthenticationComponentBase):
        def setBaseModelClass(self):
            return model.NewsComment

    class NewsBump(AuthenticationComponentBase):
        def setBaseModelClass(self):
            return model.NewsBump

    class EventType(AuthenticationComponentBase):
        def setBaseModelClass(self):
            return model.EventType

    class SchoolTeam(AuthenticationComponentBase):
        def setBaseModelClass(self):
            return model.SchoolTeam

    class Config(AuthenticationComponentBase):
        def setBaseModelClass(self):
            return model.Config

    class Score(AuthenticationComponentBase):
        def setBaseModelClass(self):
            return model.Score

    class EventActivity(AuthenticationComponentBase):
        def setBaseModelClass(self):
            return model.EventActivity

    class Event(AuthenticationComponentBase):
        def setBaseModelClass(self):
            return model.Event

    class EventTag(AuthenticationComponentBase):
        def setBaseModelClass(self):
            return model.EventTag

    class EventTeam(AuthenticationComponentBase):
        def setBaseModelClass(self):
            return model.EventTeam

    class Log(AuthenticationComponentBase):
        def setBaseModelClass(self):
            return model.Log

    class Member(AuthenticationComponentBase):
        def setBaseModelClass(self):
            return model.Member

    class MemberGroup(AuthenticationComponentBase):
        def setBaseModelClass(self):
            return model.MemberGroup

    class Region(AuthenticationComponentBase):
        def setBaseModelClass(self):
            return model.Region

    class School(AuthenticationComponentBase):
        def setBaseModelClass(self):
            return model.School

    class ScoreMapping(AuthenticationComponentBase):
        def setBaseModelClass(self):
            return model.ScoreMapping

    class Season(AuthenticationComponentBase):
        def setBaseModelClass(self):
            return model.Season

    class Summary(AuthenticationComponentBase):
        def setBaseModelClass(self):
            return model.Summary

    class Team(AuthenticationComponentBase):
        def setBaseModelClass(self):
            return model.Team
