import hashlib

from ..generalFunctions import *
from ..models import *
from ..forms import *

class Authentication:
    def __init__(self, request):
        self.request = request;

    def login(self):
        if (self.request.POST.get("email") != None and self.request.POST.get("password") != None):
            uemail = self.request.POST.get("email");
            upwd = self.request.POST.get("password");
            u = getModelObject(Account, account_email=uemail);
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
                        loghelper(self.request, "login", "Login Account id: " + str(u.id));
                        return redirect('adminIndex');
                    else:
                        return HttpResponse('{"Response": "Error: Insufficient Permission"}');
                else:
                    return HttpResponse('{"Response": "Error: Wrong Credentials"}');
        else:
            return HttpResponse('{"Response": "Error: Insufficient Parameters."}');


    @csrf_exempt
    def logout(self):
        if sessionChecker(self.request, 'uid', 'utype'):
            self.request.session['uid'] = None;
            self.request.session['utype'] = None;
            return redirect('adminIndex');
        else:
            return HttpResponse('{"Response": "Error: Not Logged In"}');
