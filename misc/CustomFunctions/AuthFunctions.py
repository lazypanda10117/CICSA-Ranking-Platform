from django.shortcuts import redirect, reverse
from django.http import Http404
from misc.CustomFunctions import RequestFunctions


def kickRequest(request, authenticated, rend):
    if signed_in(request, 'admin') or signed_in(request, 'team'):
        if authenticated:
            return rend
        else:
            return redirect(reverse('panel.index'))
    else:
        if authenticated:
            return redirect(reverse('permission.dispatch', args=['view']))
        else:
            return rend


def signed_in(request, user_type):
    return RequestFunctions.sessionChecker(request, 'uid', 'utype') and request.session['utype'] == user_type


def raise404Empty(objects=None):
    if objects is None:
        raise Http404
