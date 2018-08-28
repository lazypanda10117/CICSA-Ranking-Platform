from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from misc.CustomElements import Dispatcher
from ..base.block.Base import AbstractBlockApp
from .CustomView import CustomView
from .GeneralView import GeneralView


def index(request):
    return ManagementDataView().home(request)


@csrf_exempt
def viewDispatch(request, route, param=''):
    dispatcher = ManagementDataView().setViewDispatcher()
    view = dispatcher.get(route)(request)
    return view.dispatch(param)


class ManagementDataView(AbstractBlockApp.AppView):
    # Block App Base View Inherited Functions
    @staticmethod
    def home(request):
        # return super().index('panel.module.management_data.index', ['event'])
        return render(request, 'platform/index.html')

    def setViewDispatcher(self):
        dispatcher = Dispatcher()
        dispatcher.add('general', GeneralView)
        dispatcher.add('custom', CustomView)
        return dispatcher

    def setProcessDispatcher(self):
        pass
