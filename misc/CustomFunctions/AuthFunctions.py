import math
from django.shortcuts import redirect, reverse
from django.http import Http404
from .RequestFunctions import sessionChecker


# super bad hack
def kickRequest(request, authenticated, rend):
    return (lambda x:
            rend if math.ceil(x+0.5) else (
                lambda y: redirect(
                    reverse('permission.dispatch', args=['view'])
                ) if math.ceil(y+0.5) else redirect('panel.index')
            )(authenticated*2-1))((authenticated*2-1)*((signed_in(request, 'admin') or signed_in(request, 'team'))*2-1))


def signed_in(request, user_type):
    return sessionChecker(request, 'uid', 'utype') and request.session['utype'] == user_type


def raise404Empty(objects):
    if objects is None:
        raise Http404
