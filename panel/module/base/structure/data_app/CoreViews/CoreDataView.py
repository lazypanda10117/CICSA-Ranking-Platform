from abc import abstractmethod
from functools import partial

from api import AuthenticationMetaAPI
from misc.CustomElements import Dispatcher
from misc.CustomFunctions import MiscFunctions
from panel.component.CustomElements import Form
from panel.module.base.authentication.AuthenticationFactory import AuthenticationFactory
from panel.module.base.block.CustomComponents import PageObject, BlockSet, BlockObject
from panel.module.base.block.CustomPages import AbstractBasePage


class CoreDataView(AbstractBasePage):
    def __init__(self, request, param):
        super(request, param)
        self.authentication_meta = AuthenticationMetaAPI(self.request)
        self.authentication_type = self.authentication_meta.getAuthType()
        self.permission_obj = AuthenticationFactory(self.authentication_type).dispatch()
        # Setting up dispatchers
        self.view_dispatcher = self._setViewDispatcher()
        self.function_dispatcher = self._setFunctionDispatcher()

    @abstractmethod
    def _setViewDispatcher(self):
        pass

    @abstractmethod
    def _getTemplateBase(self):
        pass

    # TODO: Abstract template to core app
    @staticmethod
    def getPagePath():
        return 'platform/module/management_data/generate.html'

    def _setFunctionDispatcher(self):
        dispatcher = Dispatcher()
        dispatcher.add('view', self.actionView)
        dispatcher.add('add', partial(self.actionMutate, verify=False))
        dispatcher.add('edit', partial(self.actionMutate, verify=True))
        dispatcher.add('delete', partial(self.actionMutate, verify=True))
        return dispatcher

    def parseParams(self, param):
        # super().parseMatch('(\w+\s\w+)(?(\?.+))')
        param = dict(route=param)
        return param

    def genPageObject(self):
        route = self.param.get('route')
        action = self.request.GET.get("action")
        element_id = self.request.GET.get("element_id")
        page_title = (route + " " + action).title()
        route_wrapper = self.view_dispatcher.get(route)
        page_object = PageObject(
            title=page_title,
            element_list=[],
            header=[],
            external=[],
            context=dict(route=route, action=action, element_id=element_id),
        )
        # Adding additional contents to page objects
        self.function_dispatcher.get(action)(
            page_object=page_object,
            context=route_wrapper.routeClass(self.request).grabData(action=action, route=route, element_id=element_id)
        )

    def renderPage(self):
        super().renderHelper(self.genPageObject())

    def actionView(self, page_object, context):
        page_type = dict(table=True)
        page_object.context = MiscFunctions.updateDict(page_object.context, dict(type=page_type))
        page_object.element_list = BlockSet().makeBlockSet(
            BlockObject(
                block_title=None,
                element_name=None,
                header=None,
                contents=dict(
                    context=context,
                ),
            )
        )

    def actionMutate(self, page_object, context, verify):
        if verify and page_object.context.get('element_id') is None:
            raise Exception("Element ID not defined for action: {}".format(page_object.context.get('action')))

        page_type = dict(form=True)
        action = page_object.context.get('action')
        route = page_object.context.get('route')
        content = Form(
            '_{}_form'.format(action),
            route,
            action,
            self.destination,
            self.view_dispatcher.get(
                route
            ).routeForm(data=context.get('data')),
        )
        special_content = context.get('special_field')

        # Hydrating PageObject with additional data
        page_object.context = MiscFunctions.updateDict(page_object.context, dict(type=page_type))
        page_object.element_list = BlockSet().makeBlockSet(BlockObject(
            block_title=None,
            element_name=None,
            header=None,
            contents=dict(
                context=content,
                special_context=special_content
            ),
        ))