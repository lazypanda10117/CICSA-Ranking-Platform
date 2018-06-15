import json
from django.apps import apps
from ..generalFunctions import *
from ..models import *

class SearchAPI():
    def search(self, model_name, key, term):
        resultList = {};
        model = apps.get_model(app_label='ranking', model_name=model_name);
        keyDict = (lambda x: {} if x is None else json.loads(key))(key);
        termDict = (lambda x: {} if x is None else json.loads(term))(term);
        newTermDict = {};
        for key, val in termDict.items():
            newTermDict[key + '__icontains'] = val;
        searchDict = {**keyDict, **newTermDict};

        for obj in filterModelObject(model, **searchDict):
            tempDict = vars(obj);
            tempDict.pop('_state');
            id = tempDict.pop('id');
            resultList[id] = tempDict;
        return HttpResponse(json.dumps(resultList));