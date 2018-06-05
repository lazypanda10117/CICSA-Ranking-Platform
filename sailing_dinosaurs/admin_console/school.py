from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .generalFunctions import *
import hashlib, random, string

from .models import *
from .forms import *

@csrf_exempt
class SchoolView:
    def registerSchool(request):
        try:
            school_name= request.POST.get("name");
            school_email = request.POST.get("email");
            school_pwd = request.POST.get("password");
            school_region = request.POST.get("region"); #integer
            pwd_salt = ''.join(random.choices(string.ascii_uppercase + string.digits, k=15));
            hashpwd = hashlib.sha224((school_pwd + pwd_salt).encode("utf-8")).hexdigest();
            school = School(school_name=school_name, school_region=school_region, school_status="active", school_season_score=0);
            school.save();
            school_id = school.id;
            loghelper(request, "Add School id: " + school_id + " and name: " + school_name);
            school_account = Account(account_type="school", account_email=school_email, account_salt=pwd_salt, account_pwd=hashpwd, account_status="active", account_link_id=school_id);
            school_account.save();
            loghelper(request, "Add Account id: " + school_account.id + " and type: school and email: " + school_email);
        except:
            return HttpResponse('{"Response": "Error: Cannot Create School."}');
