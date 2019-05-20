import hashlib
from django.shortcuts import redirect, reverse
from django.http import HttpResponse
from cicsa_ranking.models import *
from misc.CustomFunctions import AuthFunctions, LogFunctions, ModelFunctions, RequestFunctions


class Login:
    def __init__(self, request):
        self.request = request
        self.acceptable_type = {"admin", "team"}

    @staticmethod
    def account_type_mapper(account_type):
        type_map = dict(admin="admin", school="team")
        return type_map[account_type]

    def login(self):
        post_dict = dict(self.request.POST)
        uemail = RequestFunctions.getSinglePostObj(post_dict, "email")
        upwd = RequestFunctions.getSinglePostObj(post_dict, "password")
        if uemail and upwd:
            u = ModelFunctions.getModelObject(Account, account_email=uemail)
            if u is None:
                return HttpResponse('{"Response": "Error: No Such User"}')
            else:
                u_pwd = u.account_password
                u_salt = u.account_salt
                verify_pwd = hashlib.sha224((upwd + u_salt).encode("utf-8")).hexdigest()
                if u_pwd == verify_pwd:
                    account_type = self.account_type_mapper(u.account_type)
                    if account_type in self.acceptable_type:
                        self.request.session['uid'] = u.id
                        self.request.session['utype'] = account_type
                        LogFunctions.generateLog(self.request, "system",
                                                 LogFunctions.makeLogQuery(Account, 'Login', id=u.id))
                        return redirect(reverse('panel.index'))
                    else:
                        return HttpResponse('{"Response": "Error: Insufficient Permission"}')
                else:
                    return HttpResponse('{"Response": "Error: Wrong Credentials"}')
        else:
            return HttpResponse('{"Response": "Error: Insufficient Parameters."}')

    def logout(self):
        if AuthFunctions.sessionChecker(self.request, 'uid', 'utype'):
            LogFunctions.generateLog(self.request, "system",
                                     LogFunctions.makeLogQuery(Account, 'Logout', id=self.request.session['uid']))
            self.request.session['uid'] = None
            self.request.session['utype'] = None
        else:
            print('{"Response": "Error: Not Logged In"}')
        return redirect(reverse('permission.dispatch', args=['view']))
