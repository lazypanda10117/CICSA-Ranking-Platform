from django.shortcuts import reverse, redirect
from panel.module.base.authentication.AuthenticationFactory import AuthenticationFactory
from api.authentication_api import AuthenticationMetaAPI
from api.authentication import AuthenticationGuardType
from api.authentication import AuthenticationGuard


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

    def verifyRequest(self, module, callback, failure):
        AuthenticationGuard(AuthenticationGuardType.LOGIN_GUARD, self.module_request).guard()
        if self.__checkModulePermission(module):
            return callback
        else:
            return failure if failure else redirect(reverse(self.module_base_redirect_route))
