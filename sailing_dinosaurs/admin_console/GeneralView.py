from .Dispatcher import *
from .CustomElement import *
from .generalFunctions import *

from .models import *
from .forms import *

class GeneralView:
    def __init__(self, request):
        self.view_dispatcher = self.setDispatcher();
        self.destination = 'generalProcess';
        self.session_name = 'general_view';
        self.request = request;

    def setDispatcher(self):
        dispatcher = Dispatcher();
        dispatcher.add('season', {'class': Season, 'form': SeasonForm});
        dispatcher.add('region', {'class': Region, 'form': RegionForm});
        dispatcher.add('event type', {'class': EventType, 'form': EventTypeForm});
        dispatcher.add('score mapping', {'class': ScoreMapping, 'form': ScoreMappingForm});
        dispatcher.add('log', {'class': Log, 'form': LogForm});
        return dispatcher;

    def dispatch(self, form_path):
        self.form_path = form_path;

        def generalViewDisplay():
            def actionView():
                type = dict(table=True);
                table = Table(currentClass, self.form_path).makeTable();
                content = [table];
                return dict(page_title=page_title, type=type, context=content);

            def actionAdd():
                self.request.session[self.session_name] = getViewJSON(action, None);
                type = dict(form=True);
                content = Form('_add_form', form_path, action, self.destination,
                               self.view_dispatcher.get(self.form_path)["form"]());
                return dict(page_title=page_title, type=type, context=content);

            def actionEditDelete(choice):
                choiceDict = {"edit": "_edit_form", "delete": "_delete_form"};
                if element_id is None:
                    return HttpResponse('{"Response": "Error: No Element ID Provided"}');
                else:
                    self.request.session[self.session_name] = getViewJSON(action, element_id);
                    element = currentClass.objects.get(pk=int(element_id));
                    type = dict(form=True);
                    content = Form(choiceDict[choice], form_path, action, self.destination,
                                   self.view_dispatcher.get(self.form_path)["form"](instance=element));
                    return dict(page_title=page_title, type=type, context=content);

            def setFunctionDispatcher():
                dispatcher = Dispatcher();
                dispatcher.add('view', actionView());
                dispatcher.add('add', actionAdd());
                dispatcher.add('edit', actionEditDelete('edit'));
                dispatcher.add('delete', actionEditDelete('delete'));
                return dispatcher;

            action = str(self.request.GET.get("action"));
            element_id = self.request.GET.get("element_id");

            page_title = (self.form_path + " " + action).title();
            currentData = (lambda x: x if x else None)(self.view_dispatcher.get(self.form_path));
            currentClass = currentData["class"];

            functionDispatch = setFunctionDispatcher();

            return (lambda x: render(self.request, 'console/generate.html', x) if x else
            HttpResponse('{"Response": "Error: Insufficient Parameters"}'))(functionDispatch.get(action));


        def generalViewLogic():
            def actionAdd():
                form = self.view_dispatcher.get(self.form_path)["form"](self.request.POST);
                form.save();

            def actionEdit():
                element = get_object_or_404(currentClass, pk=element_id);
                form = self.view_dispatcher.get(self.form_path)["form"](self.request.POST, instance=element);
                form.save();

            def actionDelete():
                element = get_object_or_404(currentClass, pk=element_id);
                element.delete();

            def setFunctionDispatcher():
                dispatcher = Dispatcher();
                dispatcher.add('add', actionAdd);
                dispatcher.add('edit', actionEdit);
                dispatcher.add('delete', actionDelete);
                return dispatcher;

            currentData = (lambda x: x if x else None)(self.view_dispatcher.get(self.form_path));
            currentClass = currentData["class"];

            self.request_variables = self.request.session[self.session_name];
            self.request.session[self.session_name] = None;
            action = self.request_variables["action"];
            element_id = self.request_variables["id"];

            functionDispatch = setFunctionDispatcher();
            functionDispatch.get(action)();

            return HttpResponseRedirect('general?action=view');

        return kickRequest(self.request, True,
                           (lambda x: generalViewLogic() if x else generalViewDisplay())
                           (self.request.method == 'POST'));