from django.views.decorators.csrf import csrf_exempt

from misc.CustomElements import Dispatcher
from client.CustomPages import GenericCustomPage
from client.CustomProcesses import SpecificNewsProcess


def index(request):
    return viewDispatch(request, "regattas")


def viewDispatch(request, route, param=''):
    return ClientView().viewDispatch(request, route, param)


@csrf_exempt
def processDispatch(request, route, param=''):
    return ClientView().processDispatch(request, route, param)


class ClientView():
    def setViewDispatcher(self):
        dispatcher = Dispatcher()
        dispatcher.add('scoring', GenericCustomPage)
        dispatcher.add('rotation', GenericCustomPage)
        dispatcher.add('regattas', GenericCustomPage)
        dispatcher.add('schools', GenericCustomPage)
        dispatcher.add('seasons', GenericCustomPage)
        dispatcher.add('news', GenericCustomPage)
        dispatcher.add('specific_news', GenericCustomPage)
        return dispatcher

    def setProcessDispatcher(self):
        dispatcher = Dispatcher()
        dispatcher.add('news', SpecificNewsProcess)
        return dispatcher

    def viewDispatch(self, request, dispatch_path, param=''):
        dispatcher = self.setViewDispatcher()
        page = dispatcher.get(dispatch_path)(request, dispatch_path, param)
        return page.render()

    def processDispatch(self, request, dispatch_path, param=''):
        dispatcher = self.setProcessDispatcher()
        page = dispatcher.get(dispatch_path)(request, param)
        return page.process()
