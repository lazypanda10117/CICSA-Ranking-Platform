import json
from .API import *
from ..generalFunctions import *
from ..models import *

class TeamAPI(API):
    def getTeam(self, **kwargs):
        return getModelObject(Team, **kwargs);