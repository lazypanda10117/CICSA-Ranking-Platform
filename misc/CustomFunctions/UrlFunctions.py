import json
from django.http import HttpResponseRedirect
from django.urls import reverse, resolve


def emptyActionRedirect(request, func):
    if request.GET.get('action') is None:
        current_url = resolve(request.path_info).url_name
        params = 'action=view'
        return HttpResponseRedirect(current_url + "?%s" % params)
    else:
        return func


def getModifyLink(tag, **kwargs):
    return reverse('panel.module.management_data.view_dispatch_param', args=[tag, 'custom']) + '?kwargs=' + json.dumps(kwargs)


def generateGETURL(path, arg_list):
    return path + '?' + ''.join([arg[0] + '=' + arg[1] + '&' for arg in arg_list.items()])[:-1]


def flattenRequestDict(request_dict):
    return [(key, val) for key, val in request_dict]


def getClientViewLink(path, identifier = None):
    # TODO: return reverse(path, identifier);
    return reverse(
        'client.view_dispatch', args=[path]
    ) if identifier is None else reverse(
        'client.view_dispatch_param', args=[path, identifier]
    )
