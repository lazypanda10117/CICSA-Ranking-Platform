from django.shortcuts import render
from misc.GeneralFunctions import generalFunctions as gf


def index(request):
    return gf.kickRequest(request, True, render(request, 'blackbox/platform/index.html'));