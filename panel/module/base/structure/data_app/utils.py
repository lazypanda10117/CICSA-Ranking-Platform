import json
from django.urls import reverse

from misc.CustomFunctions import APIFunctions
from misc.CustomFunctions import MiscFunctions
from misc.CustomFunctions import RequestFunctions
from misc.CustomFunctions import UrlFunctions


class QueryTermUtils:
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
        return MiscUtils.verifyRangeTerms(range_start, range_end)

    def getRedirectDestination(self, app_name, route):
        return UrlFunctions.generateGETURL(
            reverse(
                'panel.module.{}.process_dispatch_param'.format(app_name),
                args=['data', route]
            ),
            UrlFunctions.flattenRequestDict(self.request.GET)
        )


class SecurityUtils:
    def __init__(self, request):
        self.request = request

    def parseRequestPost(self):
        EXCLUDED_FIELDS = ['csrfmiddlewaretoken']
        result = dict(self.request.POST)
        for field in EXCLUDED_FIELDS:
            result.pop(field)
        return result


class MiscUtils:
    def __init__(self, request):
        self.request = request

    def useAPI(self, model):
        return APIFunctions.applyModelAPI(model, self.request)

    @staticmethod
    def verifyRangeTerms(range_start, range_end):
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

    @staticmethod
    def buildRangeTerms(range_start, range_end, result_len):
        range_start, range_end = MiscUtils.verifyRangeTerms(range_start, range_end)
        return range_start, result_len if range_end is None else range_end

    @staticmethod
    def updateChoiceAsValue(field_data, choice_data):
        temp_data = field_data
        for key, value in choice_data.items():
            temp_data[key] = MiscFunctions.grabLinkValueFromChoices(value, field_data[key])
        return temp_data

    @staticmethod
    def updateMultipleChoicesAsValues(field_data, choice_data):
        temp_data = field_data
        for key, value in choice_data.items():
            temp_data[key] = MiscFunctions.grabLinkValueFromChoices(value, field_data[key])
        return temp_data

    @staticmethod
    def updateDBMapAsValue(field_data, db_map):
        temp_data = field_data
        for key, value in db_map.items():
            temp_data[key] = value
        return temp_data
