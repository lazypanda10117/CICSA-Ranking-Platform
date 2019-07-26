from abc import ABC
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect

from misc.CustomElements import Dispatcher
from misc.CustomFunctions import AuthFunctions, MiscFunctions
from panel.component.CustomElements import Form
from panel.module.base.authentication.AuthenticationFactory import AuthenticationFactory
from panel.module.base.block.CustomProcesses import AbstractBaseProcess


class CoreDataProcess(AbstractBaseProcess):
    def __init__(self, request):
        self.request = request
        self.permission_obj = AuthenticationFactory(self.request.session['utype']).dispatch()
        self.view_dispatcher = self.setDispatcher()
        self.destination = 'custom'
        self.session_name = 'custom_view'
        self.page_path = 'platform/module/management_data/generate.html'
        self.template_base = self.getTemplateBase()

    def dispatch(self, form_path):
        self.form_path = form_path

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
