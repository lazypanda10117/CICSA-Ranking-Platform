from django.shortcuts import reverse, redirect
from api.authentication_api import AuthenticationMetaAPI
from panel.module.base.authentication.AuthenticationFactory import AuthenticationFactory


class ModulePermission:
    def __init__(self, request):
        self.module_request = request
        self.authentication_meta = AuthenticationMetaAPI(self.module_request)
        self.authentication_type = self.authentication_meta.getAuthType()
        self.authentication_class = AuthenticationFactory(self.authentication_type).dispatch()
        self.module_base_redirect_route = 'panel.index'
        self.alowed_modules = self.authentication_class.getAllowedModules()

    def __checkModulePermission(self, module):
        return module in self.alowed_modules

    def redirectRequest(self, module, callback):
        if self.__checkModulePermission(module):
            return callback
        else:
            return redirect(reverse(self.module_base_redirect_route))
