from django.views.decorators.csrf import csrf_exempt
from misc.CustomElements import Dispatcher
from panel.module.base.block.Base import AbstractBlockApp
from panel.module.management_news.CustomPages import PostPage
from panel.module.management_news.CustomPages import CommentPage
from panel.module.management_news.CustomProcesses import PostProcess
from panel.module.management_news.CustomProcesses import CommentProcess
from panel.module.ModuleRegistry import ModuleRegistry


def index(request):
    return ManagementNewsView().authenticateModule(
        request,
        ManagementNewsView().home())


def viewDispatch(request, route, param=''):
    return ManagementNewsView().authenticateModule(
        request,
        ManagementNewsView().viewDispatch(request, route, param))


@csrf_exempt
def processDispatch(request, route, param=''):
    return ManagementNewsView().authenticateModule(
        request,
        ManagementNewsView().processDispatch(request, route, param))


class ManagementNewsView(AbstractBlockApp.AppView):
    # Block App Base View Inherited Functions
    def getBaseAppName(self):
        return ModuleRegistry.MANAGEMENT_NEWS

    def home(self):
        return super().index('panel.module.management_news.view_dispatch', ['choice'])

    def setViewDispatcher(self):
        dispatcher = Dispatcher()
        dispatcher.add('post', PostPage)
        dispatcher.add('comment', CommentPage)
        return dispatcher

    def setProcessDispatcher(self):
        dispatcher = Dispatcher()
        dispatcher.add('post', PostProcess)
        dispatcher.add('comment', CommentProcess)
        return dispatcher
