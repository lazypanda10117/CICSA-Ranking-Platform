import json
from .AbstractAPI import *
from ..generalFunctions import *
from ..models import *

class SchoolAPI(AbstractAPI):
    def getSchools(self, **kwargs):
        return filterModelObject(School, **kwargs);

    def getSchool(self, **kwargs):
        return getModelObject(School, **kwargs);
