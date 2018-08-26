import math
from django.shortcuts import redirect, reverse
from django.http import Http404
from .RequestFunctions import sessionChecker


def kickRequest(request, loggedin, rend):
    return (lambda x: rend if math.ceil(x+0.5) else
    (lambda y: redirect(reverse('blackbox.permission_app.dispatch', args=['view'])) if math.ceil(y+0.5) else redirect('adminIndex'))
    (loggedin*2-1))((loggedin*2-1)*(signed_in(request, 'admin')*2-1))


def signed_in(request, user_type):
    return sessionChecker(request, 'uid', 'utype') and request.session['utype']==user_type;


def raise404Empty(objects):
    if len(objects) == 0:
        raise Http404;