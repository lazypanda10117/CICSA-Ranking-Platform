from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from misc.CustomElements import Dispatcher
from misc.CustomFunctions import AuthFunctions, MiscFunctions
from ...component.CustomElements import Form
from ..authentication.AuthenticationFactory import AuthenticationFactory


class CustomView:
    def __init__(self, request):
        self.request = request
        self.permission_obj = AuthenticationFactory(self.request.session['utype']).dispatch()
        self.view_dispatcher = self.setDispatcher()
        self.destination = 'custom'
        self.session_name = 'custom_view'
        self.page_path = 'platform/module/management_data/generate.html'
        self.template_base = self.getTemplateBase()

    def setDispatcher(self):
        dispatcher = self.permission_obj().ManagementData().getDataCustomDispatcher()
        return dispatcher

    def getTemplateBase(self):
        template_base = self.permission_obj().ManagementData().getTemplateBase()
        return template_base

    def dispatch(self, form_path):
        self.form_path = form_path

        def CustomViewDisplay():
            def loadView(actionClass):
                return (
                    lambda x: render(
                        self.request, self.page_path, MiscFunctions.updateDict(
                            x(
                                currentClass(self.request).grabData(action, form_path, element_id)
                            ), dict(auth=self.permission_obj().getIdentifier(), template_base=self.template_base))
                    ) if x else HttpResponse('{"Response": "Error: Insufficient Parameters"}'))(actionClass)

            def loadViewChecker():
                return loadView(functionDispatch.get(action)) if currentClass(self.request).dispatcher.get(
                    action) else redirect('panel.module.management_data.view_dispatch_param', form_path, 'custom')

            def actionView(data):
                action_type = dict(table=True)
                return dict(page_title=page_title, type=action_type, context=data)

            def actionAdd(data):
                self.request.session[self.session_name] = MiscFunctions.getViewJSON(action, None)
                page_type = dict(form=True)
                content = Form('_add_form', form_path, action, self.destination,
                               self.view_dispatcher.get(self.form_path)["form"](data=data['data']))
                specialContent = data['special_field']
                return dict(page_title=page_title, type=page_type, context=content, special_context=specialContent)

            def actionEdit(data):
                if element_id is None:
                    return HttpResponse('{"Response": "Error: No Element ID Provided"}')
                else:
                    self.request.session[self.session_name] = MiscFunctions.getViewJSON(action, element_id)
                    page_type = dict(form=True)
                    content = Form('_edit_form', form_path, action, self.destination,
                                   self.view_dispatcher.get(self.form_path)["form"](data=data['data']))
                    specialContent = data['special_field']
                    return dict(page_title=page_title, type=page_type, context=content, special_context=specialContent)

            def actionDelete(data):
                if element_id is None:
                    return HttpResponse('{"Response": "Error: No Element ID Provided"}')
                else:
                    self.request.session[self.session_name] = MiscFunctions.getViewJSON(action, element_id)
                    page_type = dict(form=True)
                    content = Form('_delete_form', form_path, action, self.destination,
                                   self.view_dispatcher.get(self.form_path)["form"](data=data['data']))
                    specialContent = data['special_field']
                    return dict(page_title=page_title, type=page_type, context=content, special_context=specialContent)

            def setFunctionDispatcher():
                dispatcher = Dispatcher()
                dispatcher.add('view', actionView)
                dispatcher.add('add', actionAdd)
                dispatcher.add('edit', actionEdit)
                dispatcher.add('delete', actionDelete)
                return dispatcher

            action = (lambda x: x if x else 'view')(self.request.GET.get("action"))
            element_id = self.request.GET.get("element_id")
            page_title = (self.form_path + " " + action).title()
            currentData = (lambda x: x if x else None)(self.view_dispatcher.get(self.form_path))
            currentClass = currentData["class"]

            functionDispatch = setFunctionDispatcher()

            return loadViewChecker()

        def CustomViewLogic():
            def actionAdd():
                currentClass(self.request).add()

            def actionEdit():
                currentClass(self.request).edit(element_id)

            def actionDelete():
                currentClass(self.request).delete(element_id)

            def setFunctionDispatcher():
                dispatcher = Dispatcher()
                dispatcher.add('add', actionAdd)
                dispatcher.add('edit', actionEdit)
                dispatcher.add('delete', actionDelete)
                return dispatcher

            currentData = (lambda x: x if x else None)(self.view_dispatcher.get(self.form_path))
            currentClass = currentData["class"]

            self.request_variables = self.request.session[self.session_name]
            self.request.session[self.session_name] = None
            action = self.request_variables["action"]
            element_id = self.request_variables["id"]

            functionDispatch = setFunctionDispatcher()
            functionDispatch.get(action)()
            return HttpResponseRedirect(self.destination)

        return AuthFunctions.kickRequest(
            self.request, True, (
                lambda x: CustomViewLogic() if x else CustomViewDisplay()
            )(self.request.method == 'POST'))
