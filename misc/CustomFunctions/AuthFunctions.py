from django.shortcuts import redirect, reverse
from django.http import Http404
from functools import reduce

from misc.CustomFunctions import RequestFunctions
from api.authentication import AuthenticationType


def default_session(request):
    if not RequestFunctions.sessionChecker(request, 'uid', 'utype'):
        request.session['utype'] = AuthenticationType.PUBLIC
        request.session['uid'] = -1
    return True


def is_matched(request, t):
    # The uid part guard against public access
    return default_session(request) and request.session['utype'] == t


def is_signed_in(request):
    return  default_session(request) and \
           not request.session['uid'] == -1 \
           and request.session['utype'] in [AuthenticationType.ADMIN, AuthenticationType.TEAM]


# By default, it blocks unauthenticated access and does nothing if the request is valid
# If it is an api request and it fails, it will raise an error
def kickRequest(
        request,
        rend=None,
        api=True,
        allowed_types=None,
):
    forceDefaultAuthObject(request)
    allowed_types = allowed_types if allowed_types else [AuthenticationType.ADMIN, AuthenticationType.TEAM]

    kick_result = rend
    is_request_valid = False

    matched = reduce((lambda x, y: x or y), [is_matched(request, t) for t in allowed_types])

    need_authentication = AuthenticationType.PUBLIC not in allowed_types
    public_exclusive = len(allowed_types) == 1 and allowed_types[0] == AuthenticationType.PUBLIC

    if matched:
        is_request_valid = True
    else:
        if need_authentication:
            # If the page needs authentication but your permission status is not matched, then
            # it will be sent to the login page
            kick_result = redirect(reverse('permission.dispatch', args=['view']))
        elif public_exclusive:
            # If the page is public only, but you are logged in, then
            # it will be sent to the logged in home page
            kick_result = redirect(reverse('panel.index'))
        else:
            raise Exception("There is some error with the Authentication Guard setup. This should not be reachable.")

    if is_request_valid:
        return kick_result
    if api:
        raise Exception("Insufficient Permission to Use API")
    return kick_result


def forceDefaultAuthObject(request):
    if not RequestFunctions.sessionChecker(request, 'utype'):
        request.session['utype'] = AuthenticationType.PUBLIC


def raise404Empty(objects=None):
    if objects is None:
        raise Http404
