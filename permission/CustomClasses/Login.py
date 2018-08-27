import hashlib
from django.shortcuts import redirect, reverse
from django.http import HttpResponse
from cicsa_ranking.models import *
from misc.CustomFunctions import AuthFunctions, LogFunctions, ModelFunctions, RequestFunctions

class Login:
    def __init__(self, request):
        self.request = request;

    def login(self):
        post_dict = dict(self.request.POST);
        #if (RequestFunctions.getSinglePostObj(post_dict, "email") and RequestFunctions.getSinglePostObj(post_dict, "password"):
        if (self.request.POST.get("email") is not None and self.request.POST.get("password") is not None):
            uemail = self.request.POST.get("email");
            upwd = self.request.POST.get("password");
            u = ModelFunctions.getModelObject(Account, account_email=uemail);
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
                        LogFunctions.loghelper(self.request, "system", LogFunctions.logQueryMaker(Account, 'Login', id=u.id));
                        return redirect(reverse('adminIndex')); #TODO: platform index
                    else:
                        return HttpResponse('{"Response": "Error: Insufficient Permission"}');
                else:
                    return HttpResponse('{"Response": "Error: Wrong Credentials"}');
        else:
            return HttpResponse('{"Response": "Error: Insufficient Parameters."}');

    def logout(self):
        if AuthFunctions.sessionChecker(self.request, 'uid', 'utype'):
            LogFunctions.loghelper(self.request, "system", LogFunctions.logQueryMaker(Account, 'Logout', id=self.request.session['uid']));
            self.request.session['uid'] = None;
            self.request.session['utype'] = None;
            return redirect(reverse('blackbox.permission_app.dispatch', args=['view'])); #TODO: login page
        else:
            return HttpResponse('{"Response": "Error: Not Logged In"}');
