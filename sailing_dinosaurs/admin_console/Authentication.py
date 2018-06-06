from .generalFunctions import *
import hashlib

from .models import *
from .forms import *

class Authentication:
    def __init__(self, request):
        self.request = request;

    def login(self):
        if (self.request.POST.get("email") != None and self.request.POST.get("password") != None):
            uemail = self.request.POST.get("email");
            upwd = self.request.POST.get("password");
            u = Account.objects.filter(account_email=uemail);
            if len(u) == 0:
                return HttpResponse('{"Response": "Error: No Such User"}');
            else:
                u = u.get();
                u_pwd = u.account_password;
                u_salt = u.account_salt;
                verify_pwd = hashlib.sha224((upwd + u_salt).encode("utf-8")).hexdigest();
                if u_pwd == verify_pwd:
                    self.request.session['uid'] = u.id;
                    loghelper(self.request, "login", "Login Account id: " + str(u.id));
                    if u.account_type == "admin":
                        return redirect('adminIndex');
                    else:
                        return HttpResponse('{"Response": "Error: Insufficient Permission"}');
                else:
                    return HttpResponse('{"Response": "Error: Wrong Credentials"}');
        else:
            return HttpResponse('{"Response": "Error: Insufficient Parameters."}');


    @csrf_exempt
    def logout(self):
        if self.request.session.has_key('uid'):
            self.request.session['uid'] = None;
            return redirect('adminIndex');
        else:
            return HttpResponse('{"Response": "Error: Not Logged In"}');
