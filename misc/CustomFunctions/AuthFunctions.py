from django.shortcuts import redirect, reverse
from django.http import Http404
from functools import reduce

from misc.CustomFunctions import RequestFunctions
from api.authentication import AuthenticationType 


# By default, it blocks unauthenticated access and does nothing if the request is valid
# If it is an api request and it fails, it will raise an error
def kickRequest(request, authenticated=True, rend=None, api=False, allowed_types=[AuthenticationType.ADMIN, AuthenticationType.TEAM]):
    kickResult = rend
    isValidRequest = False
    if reduce((lambda x, y: x or y), [signed_in(t) for t in allowed_types]):
        if not authenticated:
            kickResult = redirect(reverse('panel.index'))
        else:
            isValidRequest = True
    else:
        if authenticated:
            kickResult = redirect(reverse('permission.dispatch', args=['view']))
        else:
            isValidRequest = True
    
    if isValidRequest:
        return kickResult
    
    return Exception("Insufficient Permission to Use API") if api else kickResult


def signed_in(request, user_type):
    return RequestFunctions.sessionChecker(request, 'uid', 'utype') and request.session['utype'] == user_type


def raise404Empty(objects=None):
    if objects is None:
        raise Http404
