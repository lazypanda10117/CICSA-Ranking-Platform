from abc import ABC

from api.authentication import AuthenticationGuard


class CoreDataComponentConstructor(ABC):
    def __init__(self, request, app_name, base_class, mutable, guard):
        self.request = request
        self.app_name = app_name
        self.base_class = base_class
        self.mutable = mutable
        self.guard = guard
        AuthenticationGuard(self.guard, self.request).guard()
