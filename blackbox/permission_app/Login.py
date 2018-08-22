import hashlib
from django.shortcuts import render, redirect
from django.http import HttpResponse
from misc.GeneralFunctions import generalFunctions as gf
from cicsa_ranking.models import *
from blackbox.auth_app.AuthenticationFactory import AuthenticaitonFactory

class Login:
    def __init__(self, request):
        self.request = request;

    def login(self):
        if (self.request.POST.get("email") is not None and self.request.POST.get("password") is not None):
            uemail = self.request.POST.get("email");
            upwd = self.request.POST.get("password");
            u = gf.getModelObject(Account, account_email=uemail);
            if u is None:
                return HttpResponse('{"Response": "Error: No Such User"}');
            else:
                u_pwd = u.account_password;
                u_salt = u.account_salt;
                verify_pwd = hashlib.sha224((upwd + u_salt).encode("utf-8")).hexdigest();
                if u_pwd == verify_pwd:
                    if u.account_type == "admin":
                        self.request.session['uid'] = u.id;
                        self.request.session['utype'] = u.account_type;
                        self.request.session['auth'] = AuthenticaitonFactory(u.account_type).dispatch();
                        gf.loghelper(self.request, "system", gf.logQueryMaker(Account, 'Login', id=u.id));
                        return redirect('adminIndex'); #respective index page for the auth user
                    else:
                        return HttpResponse('{"Response": "Error: Insufficient Permission"}');
                else:
                    return HttpResponse('{"Response": "Error: Wrong Credentials"}');
        else:
            return HttpResponse('{"Response": "Error: Insufficient Parameters."}');

    def logout(self):
        if gf.sessionChecker(self.request, 'uid', 'utype'):
            gf.loghelper(self.request, "system", gf.logQueryMaker(Account, 'Logout', id=self.request.session['uid']));
            self.request.session['uid'] = None;
            self.request.session['utype'] = None;
            self.request.session['auth'] = None;
            return redirect('adminIndex'); #client home
        else:
            return HttpResponse('{"Response": "Error: Not Logged In"}');
