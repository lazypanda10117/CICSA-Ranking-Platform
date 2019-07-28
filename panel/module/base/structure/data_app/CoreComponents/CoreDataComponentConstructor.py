from abc import ABC


class CoreDataComponentConstructor(ABC):
    def __init__(self, request, base_class, mutable=False):
        self.request = request
        self.base_class = base_class
        self.mutable = mutable

