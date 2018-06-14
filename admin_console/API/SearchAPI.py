import json
from django.apps import apps
from ..generalFunctions import *
from ..models import *

class SearchAPI():
    def search(self, model_name, key, term):
        resultList = {};
        model = apps.get_model(app_label='ranking', model_name=model_name);
        keyDict = (lambda x: None if x is None else json.loads(key))(key);
        termDict = (lambda x: None if x is None else json.loads(term))(term);
        newTermDict = {};
        if keyDict is None:
            if termDict is None:
                searchDict = {};
            else:
                for key, val in termDict.items():
                    newTermDict[key + '__icontains'] = val;
                searchDict = newTermDict;
        else:
            if termDict is None:
                searchDict = keyDict;
            else:
                for key, val in termDict.items():
                    newTermDict[key + '__icontains'] = val;
                searchDict = {**keyDict, **newTermDict};

        for index, val in enumerate(filterModelObject(model, **searchDict)):
            tempDict = vars(val);
            tempDict.pop('_state');
            resultList[index] = tempDict;
        return HttpResponse(json.dumps(resultList));