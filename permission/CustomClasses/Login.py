import hashlib
from django.shortcuts import redirect, reverse
from django.http import HttpResponse

from api.authentication import AuthenticationType
from api.model_api import ConfigAPI
from cicsa_ranking.models import Account
from misc.CustomFunctions import LogFunctions
from misc.CustomFunctions import ModelFunctions
from misc.CustomFunctions import RequestFunctions


class Login:
    def __init__(self, request):
        self.request = request
        self.acceptable_type = [AuthenticationType.ADMIN, AuthenticationType.TEAM]

    @staticmethod
    def account_type_mapper(account_type):
        type_map = dict(admin=AuthenticationType.ADMIN, school=AuthenticationType.TEAM)
        return type_map[account_type]

    def login(self):
        post_dict = dict(self.request.POST)
        uemail = RequestFunctions.getSinglePostObj(post_dict, "email")
        upwd = RequestFunctions.getSinglePostObj(post_dict, "password")
        if uemail and upwd:
            u = ModelFunctions.getModelObject(Account, account_email=uemail)
            if u is None:
                raise Exception('User not found')
            else:
                u_pwd = u.account_password
                u_salt = u.account_salt
                verify_pwd = hashlib.sha224((upwd + u_salt).encode("utf-8")).hexdigest()
                if u_pwd == verify_pwd:
                    account_type = self.account_type_mapper(u.account_type)
                    if account_type in self.acceptable_type:
                        current_configuration = ConfigAPI(self.request).getAll()[0]
                        self.request.session['uid'] = u.id
                        self.request.session['utype'] = account_type
                        self.request.session['panel_config'] = dict(
                            season=current_configuration.config_current_season
                        )
                        LogFunctions.generateLog(self.request, "system",
                                                 LogFunctions.makeLogQuery(Account, 'Login', id=u.id))
                        return redirect(reverse('panel.index'))
                    else:
                        raise Exception('Insufficient Permission')
                else:
                    raise Exception('Wrong Credentials')
        else:
            raise Exception('Insufficient Parameters')

    def logout(self):
        if RequestFunctions.sessionChecker(self.request, 'uid', 'utype'):
            LogFunctions.generateLog(self.request, "system",
                                     LogFunctions.makeLogQuery(Account, 'Logout', id=self.request.session['uid']))
            self.request.session.clear()
            self.request.session['utype'] = AuthenticationType.PUBLIC
        else:
            raise Exception('User is not logged in')
        return redirect(reverse('permission.dispatch', args=['view']))
