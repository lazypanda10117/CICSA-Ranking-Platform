from django.views.decorators.csrf import csrf_exempt

from misc.CustomElements import Dispatcher
from client.CustomPages import GenericClientPage
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
<<<<<<< HEAD
        dispatcher.add('scoring', GenericCustomPage)
        dispatcher.add('rotation', GenericCustomPage)
        dispatcher.add('regattas', GenericCustomPage)
        dispatcher.add('schools', GenericCustomPage)
        dispatcher.add('seasons', GenericCustomPage)
        dispatcher.add('news', GenericCustomPage)
        dispatcher.add('specific_news', GenericCustomPage)
        dispatcher.add('school_details', GenericCustomPage)
=======
        dispatcher.add('scoring', GenericClientPage)
        dispatcher.add('rotation', GenericClientPage)
        dispatcher.add('regattas', GenericClientPage)
        dispatcher.add('schools', GenericClientPage)
        dispatcher.add('seasons', GenericClientPage)
        dispatcher.add('news', GenericClientPage)
        dispatcher.add('specific_news', GenericClientPage)
        dispatcher.add('league', GenericClientPage)
>>>>>>> 482e81a7c930a0150f88f417248854e459a565a2
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
