from django.shortcuts import render
from misc.CustomFunctions import AuthFunctions


def index(request):
    return AuthFunctions.kickRequest(request, render(request, 'platform/index.html'))
