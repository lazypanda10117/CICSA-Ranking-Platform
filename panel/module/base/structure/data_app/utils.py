import json

from misc.CustomFunctions import RequestFunctions, APIFunctions


class QueryTermParser:
    def __init__(self, request):
        self.request = request

    def getFilterTerms(self):
        get_dict = self.request.GET
        kwargs = RequestFunctions.getMultipleRequestObj(get_dict, 'kwargs')
        if kwargs is not None:
            kwargs = json.loads(kwargs)
            return kwargs
        return {}

    def getRangeTerms(self):
        get_dict = self.request.GET
        range_start = RequestFunctions.getMultipleRequestObj(get_dict, 'start')
        range_end = RequestFunctions.getMultipleRequestObj(get_dict, 'end')

        try:
            range_start = (int(range_start)-1 if int(range_start)-1 >= 0 else 0)
        except Exception:
            range_start = 0

        try:
            range_end = (int(range_end) if int(range_end) >= 0 else 0)
        except Exception:
            range_end = 0

        if range_end <= range_start:
            range_start = 0
            range_end = None

        return range_start, range_end


class MiscUtils:
    def __init__(self, request):
        self.request = request

    def useAPI(self, model):
        return APIFunctions.applyModelAPI(model, self.request)