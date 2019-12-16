from django.views.decorators.csrf import csrf_exempt
from ..CustomFunctions import MiscFunctions


def getSingleRequestObj(post_dict, name):
    return (lambda x: x[name][0] if name in x else None)(post_dict)


def getMultipleRequestObj(post_dict, name):
    return MiscFunctions.noneCatcher(name, post_dict)


def sessionChecker(request, *args):
    for arg in args:
        if not (arg in request.session) or request.session[arg] is None:
            return False
    return True


def sessionGetter(request, key):
    if key in request.session:
        return request.session.get(key)
    else:
        return None
