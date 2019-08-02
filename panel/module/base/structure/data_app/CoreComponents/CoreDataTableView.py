from abc import abstractmethod

from misc.CustomFunctions import UrlFunctions, MiscFunctions
from panel.component.CustomElements import Table
from panel.component.CustomElements import Button
from panel.module.base.structure.data_app.constants import ActionType
from panel.module.base.structure.data_app.utils import QueryTermUtils
from panel.module.base.structure.data_app.utils import MiscUtils
from panel.module.base.structure.data_app.CoreComponents.CoreDataComponentConstructor import CoreDataComponentConstructor


class CoreDataTableView(CoreDataComponentConstructor):
    def __init__(self, request, app_name, base_class, mutable, guard):
        super().__init__(request, app_name, base_class, mutable, guard)
        self.validation_set = self._setValidationSet()

    @abstractmethod
    def _setValidationSet(self):
        pass

    @abstractmethod
    def getHeaderContent(self):
        pass

    @abstractmethod
    def getRowContent(self, model_object):
        pass

    def render(self, **kwargs):
        route = kwargs.pop('route')
        query_term_parser = QueryTermUtils(self.request)
        table_header = self.getHeader()
        table_content = self.getBody(
            query_term_parser.getRangeTerms(), 
            **MiscFunctions.updateDict(
                query_term_parser.getFilterTerms(), self.injectTableFilter()
            )
        )
        return Table(current_class=self.base_class, title=route).buildTable(table_header, table_content)

    # Injection dict is empty bby default
    def injectTableFilter(self):
        return {}

    def getHeader(self):
        return self.getHeaderContent() + ([] if self.mutable else [ActionType.EDIT, ActionType.DELETE])

    def getBody(self, range_terms=(0, 10), **kwargs):
        result = MiscUtils(self.request).useAPI(self.base_class).filterSelf(**kwargs).order_by('id')
        range = MiscUtils.buildRangeTerms(
            range_start=range_terms[0],
            range_end=range_terms[1],
            result_len=result.count()
        )
        return [self.getRow(data) for data in result[range[0]:range[1]]]

    def getRow(self, model_object):
        row_content = dict()
        row_content["db_content"] = self.getRowContent(model_object)
        if self.mutable:
            row_content["button"] = [
                Button(
                    ActionType.EDIT.title(), 'info', UrlFunctions.generateGETURL(
                        '',
                        {"action": ActionType.EDIT, "element_id": model_object.id}
                    )
                ),
                Button(
                    ActionType.DELETE.title(), 'danger', UrlFunctions.generateGETURL(
                        '',
                        {"action": ActionType.DELETE, "element_id": model_object.id}
                    )
                ),

            ]
        return row_content
