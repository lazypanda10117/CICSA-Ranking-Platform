from django.shortcuts import render
from misc.CustomFunctions import AuthFunctions


def index(request):
    return AuthFunctions.kickRequest(request, True, render(request, 'platform/index.html'))
