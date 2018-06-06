from .generalFunctions import *
from .CustomElement import *

from .models import *
from .forms import *

class GeneralView:
    generalFormDispatch = {
        "season": {"class": Season, "form": SeasonForm},
        "region": {"class": Region, "form": RegionForm},
        "event type": {"class": EventType, "form": EventTypeForm},
        "score mapping": {"class": ScoreMapping, "form": ScoreMappingForm},
        "account": {"class": Account, "form": AccountForm},
        "log": {"class": Log, "form": LogForm},
    };

    def __init__(self, request):
        self.request = request;

    def dispatch(self, form_path):
        self.form_path = form_path;

        def generalViewDisplay():
            def actionView():
                type = dict(table=True);
                table = Table(currentClass, self.form_path).makeTable();
                content = [table];
                return dict(page_title=page_title, type=type, context=content);

            def actionAdd():
                self.request.session['general_view'] = getGeneralViewJSON(action, None);
                type = dict(form=True);
                content = Form('_add_form', form_path, action, destination,
                               self.generalFormDispatch[self.form_path]["form"]());
                return dict(page_title=page_title, type=type, context=content);

            def actionEditDelete(choice):
                choiceDict = {"edit": "_edit_form", "delete": "_delete_form"};
                if element_id is None:
                    return HttpResponse('{"Response": "Error: No Element ID Provided"}');
                else:
                    self.request.session['general_view'] = getGeneralViewJSON(action, element_id);
                    element = currentClass.objects.get(pk=int(element_id));
                    type = dict(form=True);
                    content = Form(choiceDict[choice], form_path, action, destination,
                                   self.generalFormDispatch[self.form_path]["form"](instance=element));
                    return dict(page_title=page_title, type=type, context=content);

            action = str(self.request.GET.get("action"));
            element_id = self.request.GET.get("element_id");
            page_title = (self.form_path + " " + action).title();
            destination = 'generalProcess';
            currentClass = (lambda x: self.generalFormDispatch[x]["class"] if x in self.generalFormDispatch else None)(
                self.form_path);
            functionDispatch = {"view": actionView(), "add": actionAdd(),
                                "edit": actionEditDelete("edit"), "delete": actionEditDelete("delete")};

            return render(self.request, 'console/generate.html', functionDispatch[action]) \
                if action in functionDispatch else HttpResponse('{"Response": "Error: Insufficient Parameters"}');


        def generalViewLogic():
            currentClass = (lambda x: self.generalFormDispatch[x]["class"] if x in self.generalFormDispatch else None)\
                (self.form_path);
            self.request_variables = self.request.session['general_view'];
            self.request.session['general_view'] = None;
            action = self.request_variables["action"];
            element_id = self.request_variables["id"];
            if action == 'add':
                form = self.generalFormDispatch[self.form_path]["form"](self.request.POST);
                form.save();
            elif action == 'edit':
                element = get_object_or_404(currentClass, pk=element_id);
                form = self.generalFormDispatch[self.form_path]["form"](self.request.POST, instance=element);
                form.save();
            elif action == 'delete':
                element = get_object_or_404(currentClass, pk=element_id);
                element.delete();
            return HttpResponseRedirect('general?action=view');

        return kickRequest(self.request, True,
                           (lambda x: generalViewLogic() if x else generalViewDisplay())
                           (self.request.method == 'POST'));
