from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def getSinglePostObj(post_dict, name):
    return (lambda x: x[name][0] if name in x else None)(post_dict);


@csrf_exempt
def getMultiplePostObj(post_dict, name):
    return (lambda x: x[name] if name in x else None)(post_dict);


@csrf_exempt
def sessionChecker(request, *args):
    for arg in args:
        if not (arg in request.session) or request.session[arg] is None:
            return False;
    return True;