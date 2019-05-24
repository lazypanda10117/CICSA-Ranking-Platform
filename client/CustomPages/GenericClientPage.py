import re
from django.shortcuts import render
from django.http import Http404

class GenericCustomPage():
    def __init__(self, request, path, param):
        self.request = request
        self.raw_param = param
        self.param = self.parseParams(self.raw_param)
        self.page_path = path

    def parseMatch(self, pattern):
        match = re.match(pattern, self.raw_param)
        if match:
            return match
        else:
            raise Http404("Page parameters parsing engine failed to recognize provided path")

    def parseParams(self, param):
        match = self.parseMatch('\s+')
        param = dict(type=param)
        return param

    def render():
        pass