from abc import ABC


class CoreDataComponentConstructor(ABC):
    def __init__(self, request, app_name, base_class, mutable=False):
        self.request = request
        self.app_name = app_name
        self.base_class = base_class
        self.mutable = mutable

