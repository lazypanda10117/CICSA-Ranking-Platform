from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Account, Event, Region, Season, EventActivity, EventType, Summary, Log, School, Team, MemberGroup, Member
from django.utils import timezone
import numpy as np
import hashlib, random, string, rsa, requests, datetime, json
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.http import QueryDict


def index(request):
    return HttpResponse("This is the index page of a CICSA Ranking Platform.");

def loghelper(request, message):
    log = Log(log_creator=request.session['uid'], log_type="admin", log_content=message);
    log.save();

@csrf_exempt
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

@csrf_exempt
def login(request):
    if (request.POST.get("email") != None and request.POST.get("password") != None):
        uemail = request.POST.get("email");
        upwd = request.POST.get("password");
        u = Account.objects.filter(account_email=uemail);
        if len(u) == 0:
            return HttpResponse('{"Response": "Error: No Such User"}');
        else:
            u = u.get();
            u_pwd = u.user_pwd;
            u_salt = u.user_hash_salt;
            verify_pwd = hashlib.sha224((upwd + u_salt).encode("utf-8")).hexdigest();
            if u_pwd == verify_pwd:
                request.session['uid'] = u.id;
                Log(log_creator=request.session['uid'], log_type="login", log_content="Login Account id: " + u.id).save();
                if u.account_type == "admin":
                    return redirect('../console/admin/');
                else:
                    return redirect('../console/school/');
            else:
                return HttpResponse('{"Response": "Error: Wrong Credentials"}');
    else:
        return HttpResponse('{"Response": "Error: Insufficient Parameters."}');


@csrf_exempt
def logout(request):
    if request.session.has_key('uid'):
        request.session['uid'] = None;
        return redirect('../home/');
    else:
        return HttpResponse('{"Response": "Error: Not Logged In"}');


@csrf_exempt
def permission(request):
    signed_in = True if (request.session.has_key('uid') and request.session['uid']!= None) else False;
    return render(request, 'template/login.html', {'signedIn': signed_in});
