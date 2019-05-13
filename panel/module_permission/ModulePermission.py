from django.shortcuts import reverse, redirect
from api.authentication_api.AuthenticationMetaAPI import AuthenticationMetaAPI


class ModulePermission:
    def __init__(self, request):
        self.module_request = request
        self.authentication_meta = AuthenticationMetaAPI(self.module_request)
        self.module_base_redirect_route = 'panel.index'
        self.allowed_modules = dict(
            Admin=dict(
                DataModule=True,
                AdminEventModule=True,
                RankingModule=True,
                NewsModule=True
            ),
            Team=dict(
                DataModule=False,
                AdminEventModule=False,
                RankingModule=True,
                NewsModule=False
            )
        )

    def __checkModulePermission(self, module):
        auth_type = self.authentication_meta.getAuthType()
        if auth_type in self.allowed_modules:
            if module in self.allowed_modules.get(auth_type):
                return self.allowed_modules.get(auth_type).get(module)
        return False

    def redirectRequest(self, module, callback):
        if self.__checkModulePermission(module):
            return callback
        else:
            return redirect(reverse(self.module_base_redirect_route))
