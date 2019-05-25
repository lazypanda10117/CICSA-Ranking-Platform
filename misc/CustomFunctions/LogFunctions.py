from cicsa_ranking.models import *
from .MiscFunctions import filterDict
from .ModelFunctions import getModelObject


def generateLog(request, log_type, message):
    log = Log(log_creator=request.session['uid'], log_type=log_type, log_content=message)
    log.save()


def makeLogQuery(model_name, log_type, **kwargs):
    return makeLogQueryFromObject(model_name, log_type, getModelObject(model_name, **kwargs))


def makeLogQueryFromObject(model_name, log_type, obj):
    invalid = {'_state'}
    log = log_type + ' ' + str(model_name.__name__) + ' - '
    item_dict = filterDict(obj.__dict__.items(), invalid)
    for key in item_dict:
        log += str(key) + ': ' + str(item_dict[key]) + ', '
    return log[:-2]
