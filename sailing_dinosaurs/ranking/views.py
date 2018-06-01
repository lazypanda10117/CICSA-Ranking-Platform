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
