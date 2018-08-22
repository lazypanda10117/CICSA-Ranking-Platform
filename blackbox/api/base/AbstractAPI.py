from abc import ABC, abstractmethod


# not much use of a class right now, but might be more useful later
class AbstractAPI():
    def __init__(self, request):
        self.request = request;
        self.auth = self.request['auth'];
