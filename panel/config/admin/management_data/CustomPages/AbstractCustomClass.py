from abc import ABC
from panel.component.CustomElements import Button
from misc.CustomFunctions import UrlFunctions
from .ImmutableBase import ImmutableBase


class AbstractCustomClass(ImmutableBase, ABC):
    def setViewDispatcher(self):
        dispatcher = super().setViewDispatcher()
        dispatcher.update('edit', True)
        dispatcher.update('delete', True)
        return dispatcher

    # Table Generating Functions
    def getTableHeader(self):
        return self.getTableSpecificHeader() + ["edit", "delete"]

    def getTableRow(self, content):
        rowContent = dict()
        rowContent["db_content"] = self.getTableRowContent(content)
        rowContent["button"] = self.makeEditDeleteBtn('custom', str(content.id))
        return rowContent

    @staticmethod
    def makeEditDeleteBtn(path, id):
        editBtn = Button('Edit', 'info', UrlFunctions.generateGETURL(path, {"action": 'edit', "element_id": id}))
        deleteBtn = Button('Delete', 'danger', UrlFunctions.generateGETURL(path, {"action": 'delete', "element_id": id}))
        return [editBtn, deleteBtn]
