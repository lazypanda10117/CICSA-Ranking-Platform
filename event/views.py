from django.shortcuts import render, HttpResponse, redirect, reverse

from .models import *
from .forms import *

def index(request):
    return redirect(reverse('eventChoice'));

def choice(request):
    return render(request, 'console/event.html');

def eventFactory(request):
    return HttpResponse('in progress');