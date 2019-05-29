import re
from django.shortcuts import render
from django.http import Http404

from misc.CustomElements import Dispatcher
from api.client_api.page_api import *


class GenericClientPage():
    def __init__(self, request, path, param):
        self.request = request
        self.path = path
        self.raw_param = param
        self.param = self.parseParams(self.raw_param)
        self.dispatcher = self.setDispatcher()

    def setDispatcher(self):
        dispatcher = Dispatcher()
        dispatcher.add('scoring', dict(page_api=ScoringPageAPI, template_path='client/regatta.html'))
        dispatcher.add('rotation', dict(page_api=RotationPageAPI, template_path='client/rotation.html'))
        dispatcher.add('regattas', dict(page_api=RegattasPageAPI, template_path='client/regattas.html'))
        dispatcher.add('schools', dict(page_api=SchoolsPageAPI, template_path='client/teams.html'))
        dispatcher.add('seasons', dict(page_api=SeasonPageAPI, template_path='client/seasons.html'))
        dispatcher.add('news', dict(page_api=NewsPageAPI, template_path='client/news.html'))
        dispatcher.add('specific_news', dict(page_api=SpecificNewsPageAPI, template_path='client/specific_news.html'))
        dispatcher.add('league', dict(page_api=LeaguePageAPI, template_path='client/league.html'))
        return dispatcher

    def parseMatch(self, pattern):
        match = re.match(pattern, self.raw_param)
        if match:
            return match
        else:
            raise Http404("Page parameters parsing engine failed to recognize provided path")

    def parseParams(self, param):
        self.parseMatch('^(\s*|\d+)$')
        if param:
            param = dict(id=param)
        else:
            param = dict()
        return param

    def render(self):
        page_data = self.dispatcher.get(self.path)["page_api"](self.request).grabPageData(**self.param)
        return render(self.request, self.dispatcher.get(self.path)["template_path"], dict(page_data=page_data))
