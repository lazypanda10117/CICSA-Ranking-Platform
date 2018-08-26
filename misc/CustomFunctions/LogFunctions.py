from cicsa_ranking.models import *
from .MiscFunctions import filterDict
from .ModelFunctions import getModelObject


def loghelper(request, log_type, message):
    log = Log(log_creator=request.session['uid'], log_type=log_type, log_content=message);
    log.save();


def logQueryMaker(model_name, type, **kwargs):
    invalid = {'_state'};
    log = type + ' ' + str(model_name.__name__) + ' - ';
    item_dict = filterDict(getModelObject(model_name, **kwargs).__dict__.items(), invalid);
    for key in item_dict:
        log += str(key) + ': ' + str(item_dict[key]) + ', ';
    return log[:-2];