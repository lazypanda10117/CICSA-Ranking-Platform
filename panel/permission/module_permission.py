class ModulePermission:
    def __init__(self, request):
        self.authentication_type = request
        self.allowed_modules = dict(
            admin=dict(),
            team=dict()
        )
        self.module_base_redirect_route = ''

    def __checkModulePermission(self, route):
        return True

    def rerouteRequest(self, route):
        if self.__checkModulePermission(route):
            return route
        else:
            return self.module_base_redirect_route