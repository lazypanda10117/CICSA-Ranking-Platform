from abc import ABC
from abc import abstractmethod

from misc.CustomFunctions import MiscFunctions
from misc.CustomFunctions import UrlFunctions
from panel.component.CustomElements import Table
from panel.component.CustomElements import Button
from panel.module.base.structure.data_app.CoreComponents.CoreDataComponentConstructor import \
    CoreDataComponentConstructor
from panel.module.base.structure.data_app.constants import ActionType
from panel.module.base.structure.data_app.utils import QueryTermParser
from panel.module.base.structure.data_app.utils import MiscUtils


class CoreDataTableView(CoreDataComponentConstructor):
    def getTableHeader(self):
        return self.getTableSpecificHeader()

    @abstractmethod
    def getTableSpecificHeader(self):
        pass

    def getTableRow(self, content):
        rowContent = dict()
        rowContent["db_content"] = self.getTableRowContent(content)
        rowContent["button"] = self.makeEditDeleteBtn('custom', str(content.id))
        return rowContent

    @abstractmethod
    def getTableRowContent(self, content):
        pass

    @staticmethod
    def updateChoiceAsValue(field_data, choice_data):
        temp_data = field_data
        for key, value in choice_data.items():
            temp_data[key] = MiscFunctions.grabLinkValueFromChoices(value, field_data[key])
        return temp_data

    @staticmethod
    def updateMultipleChoicesAsValues(field_data, choice_data):
        temp_data = field_data
        for key, value in choice_data.items():
            temp_data[key] = MiscFunctions.grabLinkValueFromChoices(value, field_data[key])
        return temp_data

    @staticmethod
    def updateDBMapAsValue(field_data, db_map):
        temp_data = field_data
        for key, value in db_map.items():
            temp_data[key] = value
        return temp_data

    def getTableContent(self, range_terms=(0, 10), **kwargs):
        result = sorted(
                MiscUtils(self.request).useAPI(self.base_class).filterSelf(**kwargs),
                key=lambda q: q.id
            )
        result_length = len(result)
        return [
            self.getTableRow(content) for content in
            result[
                range_terms[0]:
                (range_terms[1] if ((range_terms[1] is not None) and (range_terms[1] < result_length)) else result_length)
            ]
        ]

    def grabTableData(self, route):
        query_term_parser = QueryTermParser(self.request)
        table_header = self.getTableHeader()
        table_content = self.getTableContent(query_term_parser.getRangeTerms(), **query_term_parser.getFilterTerms())
        table = Table(currentClass=self.base_class, title=route).makeCustomTables(table_header, table_content)
        return [table]

    def getTableHeader(self):
        return self.getTableSpecificHeader() if self.mutable else self.getTableSpecificHeader() + [ActionType.EDIT, ActionType.DELETE]

    def makeEditDeleteBtn(self, path, element_id):
        editBtn = Button(
            'Edit', 'info', UrlFunctions.generateGETURL(
                path,
                {"action": ActionType.EDIT, "element_id": element_id}
            )
        )
        deleteBtn = Button(
            'Delete', 'danger', UrlFunctions.generateGETURL(
                path,
                {"action": ActionType.DELETE, "element_id": element_id}
            )
        )
        return [editBtn, deleteBtn]
