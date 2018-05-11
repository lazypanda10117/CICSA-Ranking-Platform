from django.shortcuts import render
from django.http import HttpResponse

def index():
    return HttpResponse("hello world");
