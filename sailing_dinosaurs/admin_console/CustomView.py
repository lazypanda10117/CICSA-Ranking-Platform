from .generalFunctions import *
from .CustomElement import *

from .models import *
from .forms import *

customViewDispatch = {
    "school": {"class": School,"form": SchoolForm},

};
class CustomView:
    def __init__(self, request):
        self.request = request;

    def dispatch(self, form_path):
        def customViewDisplay():
            def actionView():
                type = dict(table=True);
                table = Table(currentClass, self.form_path).makeTable();
                content = [table];
                return dict(page_title=page_title, type=type, context=content);