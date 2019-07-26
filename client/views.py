from django.views.decorators.csrf import csrf_exempt

from misc.CustomElements import Dispatcher
from client.CustomPages import GenericClientPage
from client.CustomProcesses import SpecificNewsProcess


def index(request):
    return viewDispatch(request, "events")


def viewDispatch(request, route, param=''):
    return ClientView().viewDispatch(request, route, param)


@csrf_exempt
def processDispatch(request, route, param=''):
    return ClientView().processDispatch(request, route, param)


class ClientView():
    def setViewDispatcher(self):
        dispatcher = Dispatcher()
        dispatcher.add('events', GenericClientPage)
        dispatcher.add('event_scoring', GenericClientPage)
        dispatcher.add('event_rotation', GenericClientPage)
        dispatcher.add('league', GenericClientPage)
        dispatcher.add('schools', GenericClientPage)
        dispatcher.add('school_specific', GenericClientPage)
        dispatcher.add('seasons', GenericClientPage)
        dispatcher.add('news', GenericClientPage)
        dispatcher.add('news_specific', GenericClientPage)
        return dispatcher

    def setProcessDispatcher(self):
        dispatcher = Dispatcher()
        dispatcher.add('news', SpecificNewsProcess)
        return dispatcher

    def viewDispatch(self, request, dispatch_path, param=''):
        dispatcher = self.setViewDispatcher()
        page = dispatcher.get(dispatch_path)(request, dispatch_path, param)
        return page.renderPage()

    def processDispatch(self, request, dispatch_path, param=''):
        dispatcher = self.setProcessDispatcher()
        page = dispatcher.get(dispatch_path)(request, param)
        return page.process()
