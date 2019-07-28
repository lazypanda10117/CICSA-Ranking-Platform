from abc import abstractmethod
from functools import partial

from misc.CustomElements import Dispatcher
from misc.CustomFunctions import MiscFunctions
from panel.module.base.block.CustomComponents import PageObject
from panel.module.base.block.CustomComponents import BlockSet
from panel.module.base.block.CustomComponents import BlockObject
from panel.module.base.block.CustomPages import AbstractBasePage


class CoreDataView(AbstractBasePage):
    def __init__(self, request, param):
        super().__init__(request, param)
        self.app_name = self._setAppName()
        self.view_dispatcher = self._setViewDispatcher()
        self.function_dispatcher = self._setFunctionDispatcher()

    @abstractmethod
    def _setAppName(self):
        pass

    @abstractmethod
    def _setViewDispatcher(self):
        pass

    def getPagePath(self):
        return 'platform/module/management_data/generate.html'

    def _setFunctionDispatcher(self):
        dispatcher = Dispatcher()
        dispatcher.add('view', self.actionView)
        dispatcher.add('add', partial(self.actionMutate, verify=False))
        dispatcher.add('edit', partial(self.actionMutate, verify=True))
        dispatcher.add('delete', partial(self.actionMutate, verify=True))
        return dispatcher

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
        element_id = page_object.context.get('element_id')
        action = page_object.context.get('action')
        route = page_object.context.get('route')

        if verify and element_id is None:
            raise Exception("Element ID not defined for action {} at {}".format(action, route))

        # Hydrating PageObject with additional data
        page_type = dict(form=True)
        page_object.context = MiscFunctions.updateDict(page_object.context, dict(type=page_type))
        page_object.element_list = BlockSet().makeBlockSet(BlockObject(
            block_title=None,
            element_name=None,
            header=None,
            contents=dict(
                context=context,
            ),
        ))

    def genPageObject(self):
        route = self.param.get('route')
        action = self.request.GET.get("action")
        element_id = self.request.GET.get("element_id")
        page_title = (route + " " + action).title()
        route_component = self.view_dispatcher.get(route)
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
            context=route_component(self.request).generateData(
                action=action, route=route, element_id=element_id, app_name=self.app_name
            )
        )

    def render(self):
        super().renderHelper(self.genPageObject())

    def parseParams(self, param):
        super().parseMatch('[\w|\d]+')
        param = dict(route=param)
        return param
