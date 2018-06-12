from django.shortcuts import render, redirect
from django.http import HttpResponse

def index(request):
    return HttpResponse("This is the index page of a CICSA Ranking Platform.");
