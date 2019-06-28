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
        rend=None,
        api=False,
        allowed_types=None
):
    allowed_types = allowed_types if allowed_types else [AuthenticationType.ADMIN, AuthenticationType.TEAM]
    kick_result = rend
    is_request_valid = False
    if reduce((lambda x, y: x or y), [signed_in(request, t) for t in allowed_types]):
        if not authenticated:
            kick_result = redirect(reverse('panel.index'))
        else:
            is_request_valid = True
    else:
        if authenticated:
            kick_result = redirect(reverse('permission.dispatch', args=['view']))
        else:
            is_request_valid = True
    
    if is_request_valid:
        return kick_result
    
    return Exception("Insufficient Permission to Use API") if api else kick_result


def signed_in(request, user_type):
    return RequestFunctions.sessionChecker(request, 'uid', 'utype') and request.session['utype'] == user_type


def raise404Empty(objects=None):
    if objects is None:
        raise Http404
