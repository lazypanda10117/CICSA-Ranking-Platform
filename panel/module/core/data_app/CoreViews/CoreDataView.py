from abc import ABC
from django.shortcuts import render, redirect
from django.http import HttpResponse

from api import AuthenticationMetaAPI
from misc.CustomElements import Dispatcher
from misc.CustomFunctions import MiscFunctions
from panel.component.CustomElements import Form
from panel.module.base.authentication.AuthenticationFactory import AuthenticationFactory
from panel.module.base.block.CustomComponents import PageObject
from panel.module.base.block.CustomPages import AbstractBasePage


class CoreDataView(AbstractBasePage):
    def __init__(self, request, param):
        super(request, param)
        self.authentication_meta = AuthenticationMetaAPI(self.request)
        self.authentication_type = self.authentication_meta.getAuthType()
        self.permission_obj = AuthenticationFactory(self.authentication_type).dispatch()

        self.view_dispatcher = self.setDispatcher()
        self.destination = 'custom'
        self.session_name = 'custom_view'

        self.template_base = self.getTemplateBase()

    def parseParams(self, param):
        # super().parseMatch('(\w+\s\w+)(?(\?.+))')
        param = dict(route=param)
        return param

    def genPageObject(self):
        route = self.param.get('route')
        action = (lambda x: x if x else 'view')(self.request.GET.get("action"))
        element_id = self.request.GET.get("element_id")
        page_title = (self.form_path + " " + action).title()
        currentData = self.view_dispatcher.get(route)
        currentClass = currentData["class"]
        functionDispatch = setFunctionDispatcher()

        currentClass(self.request).grabData(action, form_path, element_id)

        return PageObject('Event Related Objects List', self.generateList(), [])

    def render(self):
        super().renderHelper(self.genPageObject())


    @staticmethod
    def getPagePath():
        return 'platform/module/management_data/generate.html'

    def setDispatcher(self):
        dispatcher = self.permission_obj().ManagementData().getDataCustomDispatcher()
        return dispatcher

    def getTemplateBase(self):
        template_base = self.permission_obj().ManagementData().getTemplateBase()
        return template_base

    def setFunctionDispatcher(self):
        dispatcher = Dispatcher()
        dispatcher.add('view', self.actionView)
        dispatcher.add('add', self.actionAdd)
        dispatcher.add('edit', self.actionEdit)
        dispatcher.add('delete', self.actionDelete)
        return dispatcher

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



        action = (lambda x: x if x else 'view')(self.request.GET.get("action"))
        element_id = self.request.GET.get("element_id")
        page_title = (self.form_path + " " + action).title()
        currentData = (lambda x: x if x else None)(self.view_dispatcher.get(self.form_path))
        currentClass = currentData["class"]

        functionDispatch = setFunctionDispatcher()

        return loadViewChecker()



