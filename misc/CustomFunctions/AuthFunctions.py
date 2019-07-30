from django.shortcuts import redirect, reverse
from django.http import Http404
from functools import reduce

from misc.CustomFunctions import RequestFunctions
from api.authentication import AuthenticationType


# By default, it blocks unauthenticated access and does nothing if the request is valid
# If it is an api request and it fails, it will raise an error
def kickRequest(
    request,
    authenticated=True,
    callback=None,
    api=False,
    allowed_types=None,
):
    forceDefaultAuthObject(request)
    allowed_types = allowed_types if allowed_types else [AuthenticationType.ADMIN, AuthenticationType.TEAM]
    kick_result = callback
    is_request_valid = False

    if reduce((lambda x, y: x or y), [authTypeChecker(request, t) for t in allowed_types]):
        if not authenticated:
            kick_result = redirect(reverse('panel.index'))
        else:
            is_request_valid = True
    else:
        if authenticated:
            kick_result = redirect(reverse('permission.dispatch', args=['view']))
        else:
            is_request_valid = True

    if not api:
        return kick_result

    if not is_request_valid:
        raise Exception("Insufficient Permission to Use API")


def forceDefaultAuthObject(request):
    if not RequestFunctions.sessionChecker(request, 'utype'):
        request.session['utype'] = AuthenticationType.PUBLIC


def authTypeChecker(request, user_type):
    return RequestFunctions.sessionChecker(request, 'utype') and request.session['utype'] == user_type


def raise404Empty(objects=None):
    if objects is None:
        raise Http404
