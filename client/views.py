from django.shortcuts import render
from django.http import Http404, HttpResponse
from api.client_api import ScoringAPI
import json


def test(request, param):
    response = ScoringAPI(request).grabPageData(id=int(param))
    return HttpResponse(json.dumps(response))



