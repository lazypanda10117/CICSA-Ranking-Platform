from abc import ABC, abstractmethod

from .Dispatcher import Dispatcher
from .generalFunctions import *
from .CustomElement import *

from .models import *
from .forms import *

class AbstractCustomClass(ABC):

    def __init__(self, request, base_class):
        self.dispatcher = self.setDispatcher();
        self.request = request;
        self.base_class = base_class;

    def setDispatcher(self):
        dispatcher = Dispatcher();
        dispatcher.add('add', self.grabFormData);
        dispatcher.add('edit', self.grabFormData);
        dispatcher.add('delete', self.grabFormData);
        dispatcher.add('view', self.grabTableData);
        return dispatcher;


    ###
    ### View Process Functions
    ###

    @abstractmethod
    def add(self):
        pass;

    @abstractmethod
    def edit(self, id):
        pass;

    @abstractmethod
    def delete(self, id):
        pass;


    ###
    ### View Generating Functions
    ###

    @abstractmethod
    def grabFormData(self, action):
            pass;

    @abstractmethod
    def getTableHeader(self):
        pass;

    @abstractmethod
    def getTableRow(self,content):
        rowContent = {};
        rowContent["db_content"] = '';
        rowContent["button"] = self.makeEditDeleteBtn('custom', str(content.id));
        pass;

    @abstractmethod
    def makeEditDeleteBtn(self, path, id):
        editBtn = Button('Edit', 'info', generateGETURL(path, {"action": 'edit', "element_id": id}));
        deleteBtn = Button('Delete', 'danger', generateGETURL(path, {"action": 'delete', "element_id": id}))
        return [editBtn, deleteBtn];

    @abstractmethod
    def getTableContent(self):
        return [self.getTableRow(content) for content in self.base_class.objects.all()];

    @abstractmethod
    def grabTableData(self, form_path):
        tableHeader = self.getTableHeader();
        tableContent = self.getTableContent();
        table = Table(self.base_class, form_path).makeCustomTables(tableHeader, tableContent);
        return [table];

    @abstractmethod
    def grabData(self, action, form_path):
        return (lambda x: x(form_path if action == 'view' else action) if x else None)\
            (self.dispatcher.get(action))

