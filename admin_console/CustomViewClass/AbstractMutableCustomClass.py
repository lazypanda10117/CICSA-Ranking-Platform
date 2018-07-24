from abc import abstractmethod

from .AbstractImmutableCustomClass import *
from ..HelperClass import *
from ..generalFunctions import *

from ..models import *
from ..forms import *

class AbstractMutableCustomClass(AbstractImmutableCustomClass):

    def __init__(self, request, base_class, validation_table):
        self.dispatcher = self.setViewDispatcher();
        self.request = request;
        self.base_class = base_class;
        self.validation_table = validation_table;

    def setViewDispatcher(self):
        dispatcher = super().setViewDispatcher();
        dispatcher.update('edit', True);
        dispatcher.update('delete', True);
        return dispatcher;

    ### Table Generating Functions
    def getTableHeader(self):
        return self.getTableSpecificHeader() + ["edit", "delete"];

    def getTableRow(self, content):
        rowContent = {};
        rowContent["db_content"] = self.getTableRowContent(content);
        rowContent["button"] = self.makeEditDeleteBtn('custom', str(content.id));
        return rowContent;

    def makeEditDeleteBtn(self, path, id):
        editBtn = Button('Edit', 'info', generateGETURL(path, {"action": 'edit', "element_id": id}));
        deleteBtn = Button('Delete', 'danger', generateGETURL(path, {"action": 'delete', "element_id": id}))
        return [editBtn, deleteBtn];
