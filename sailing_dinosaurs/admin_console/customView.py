from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .generalFunctions import *

from .models import *
from .forms import *

generalFormDispatch = {
    "season": {"class": Season,"form": SeasonForm},
    "region": {"class": Region,"form": RegionForm},
    "event type": {"class": EventType, "form": EventTypeForm},
    "score mapping": {"class": ScoreMapping, "form": ScoreMappingForm}
};

def customView(request, form_path):

    def generateGETURL(path, argList):
        return path + '?' + ''.join([arg[0]+'='+arg[1]+'&' for arg in argList.items()])[:-1];

    def getPageTitle(action):
        return (form_path + " " + action).title();

    def getFormID(form_string):
        return form_path + form_string;

    def getGeneralViewJSON(action, id):
        return {"action": action, "id": id};

    def getTableElement(currentClass):
        def makeAddBtn(path):
            addBtn = {"title": 'Add', "style": 'success', "redirect": generateGETURL(path, {"action": 'add'})};
            return dict(add_button = addBtn);
        return makeAddBtn('general');

    def getTableHeader(currentClass):
        fields = [field.name for field in currentClass._meta.get_fields()];
        fields += ["edit", "delete"];
        return fields;

    def getTableContent(currentClass):
        def makeEditDeleteBtn(path, id):
            editBtn = {"title": 'Edit', "style": 'info', "redirect": generateGETURL(path, {"action": 'edit', "element_id": id})};
            deleteBtn = {"title": 'Delete', "style": 'danger', "redirect": generateGETURL(path, {"action": 'delete', "element_id": id})};
            return [editBtn, deleteBtn];

        def getTableRow(content):
            rowContent = {"db_content": list(vars(content).values())[1:], "button": makeEditDeleteBtn('general', str(content.id))};
            return rowContent;

        return [getTableRow(content) for content in currentClass.objects.all()];

    def customViewDisplay():
        action = str(request.GET.get("action"));
        element_id = request.GET.get("element_id");
        page_title = getPageTitle(action);
        destination = 'process';
        currentClass = (lambda x: generalFormDispatch[x]["class"] if x in generalFormDispatch else None)(form_path);
        if action == 'view':
            type = dict(table=True);
            tableElement = getTableElement(currentClass);
            tableHeader = getTableHeader(currentClass);
            tableContent = getTableContent(currentClass);
            table = dict(title=form_path, tableElement=tableElement, tableHeader=tableHeader, tableContent=tableContent);
            return render(request, 'console/generate.html',
                          dict(page_title=page_title, type=type, context=[table]));
        elif action == 'add':
            request.session['general_view'] = getGeneralViewJSON(action, None);
            type = dict(form=True);
            content = dict(form_id=getFormID('_add_form'), form_action=action.title(), destination=destination, form=generalFormDispatch[form_path]["form"]());
            return render(request, 'console/generate.html',
                                                     dict(page_title=page_title, type=type, context=content));
        elif action == 'edit':
            if element_id is None:
                return HttpResponse('{"Response": "Error: No Element ID Provided"}');
            else:
                request.session['general_view'] = getGeneralViewJSON(action, element_id);
                element = currentClass.objects.get(pk=int(element_id));
                type = dict(form=True);
                content = dict(form_id=getFormID('_edit_form'), form_action=action.title(), destination=destination,
                               form=generalFormDispatch[form_path]["form"](instance=element));
                return render(request, 'console/generate.html',
                                                         dict(page_title=page_title, type=type, context=content));
        elif action == 'delete':
            if element_id is None:
                return HttpResponse('{"Response": "Error: No Element ID Provided"}');
            else:
                request.session['general_view'] = getGeneralViewJSON(action, element_id);
                element = currentClass.objects.get(pk=int(element_id));
                type = dict(form=True);
                content = dict(form_id=getFormID('_edit_form'), form_action=action.title(), destination=destination,
                               form=generalFormDispatch[form_path]["form"](instance=element));
                return render(request, 'console/generate.html',
                                                         dict(page_title=page_title, type=type, context=content));
        else:
            return HttpResponse('{"Response": "Error: Invalid Action"}');

    def customViewLogic():
        customViewDispatch = {"school": {"add": '', "edit": ''}};
        currentClass = (lambda x: generalFormDispatch[x]["class"] if x in generalFormDispatch else None)(form_path);
        request_variables = request.session['general_view'];
        request.session['general_view'] = None;
        action = request_variables["action"];
        element_id = request_variables["id"];
        if action == 'add':
            form = generalFormDispatch[form_path]["form"](request.POST);
            form.save();
        elif action == 'edit':
            element = get_object_or_404(currentClass, pk=element_id);
            form = generalFormDispatch[form_path]["form"](request.POST, instance=element);
            form.save();
        elif action == 'delete':
            element = get_object_or_404(currentClass, pk=element_id);
            element.delete();
        return HttpResponseRedirect('general?action=view');

    return kickRequest(request, True,
                       (lambda x: customViewLogic() if x else customViewDisplay())
                       (request.method == 'POST'));

@csrf_exempt
def kickRequest(request, loggedin, rend):
    return (lambda x: rend if math.ceil(x+0.5) else (lambda y: redirect('../admin/permission') if math.ceil(y+0.5) else redirect('../admin')) (loggedin*2-1))((loggedin*2-1)*(signed_in(request)*2-1))
