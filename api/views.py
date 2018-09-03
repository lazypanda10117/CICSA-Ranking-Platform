from .functional_api import *


def search(request):
    item = request.GET.get("item")
    key = request.GET.get("key")
    term = request.GET.get("term")
    return SearchAPI(request).search(item, key, term)
