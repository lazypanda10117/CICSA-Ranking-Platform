import math
from django.shortcuts import redirect, reverse
from django.http import Http404
from .RequestFunctions import sessionChecker


def kickRequest(request, authenticated, rend):
    return (lambda x:
            rend if math.ceil(x+0.5) else (
                lambda y: redirect(
                    reverse('permission.dispatch', args=['view'])
                ) if math.ceil(y+0.5) else redirect('adminIndex')
            )(authenticated*2-1))((authenticated*2-1)*(signed_in(request, 'admin')*2-1))


def signed_in(request, user_type):
    return sessionChecker(request, 'uid', 'utype') and request.session['utype'] == user_type


def raise404Empty(objects):
    if len(objects) == 0:
        raise Http404
