import json
from .AbstractAPI import *
from ..generalFunctions import *
from ..models import *

class TeamAPI(AbstractAPI):
    def getTeam(self, **kwargs):
        return getModelObject(Team, **kwargs);