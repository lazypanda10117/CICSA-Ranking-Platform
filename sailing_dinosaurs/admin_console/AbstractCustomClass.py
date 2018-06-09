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

### View Process Functions

    @abstractmethod
    def add(self):
        pass;

    @abstractmethod
    def edit(self, id):
        pass;

    @abstractmethod
    def delete(self, id):
        pass;

### View Generating Functions

    @abstractmethod
    def grabData(self, *args):
        #args[0] = action, args[1] = form_path, args[2] = element_id
        if args[0] == 'view':
            return self.dispatcher.get(args[0])(form_path = args[1]);
        elif args[0] == 'add':
            return self.dispatcher.get(args[0])(action=args[0], element_id=args[2]);
        elif args[0] == 'edit':
            if args[2]:
                return self.dispatcher.get(args[0])(action=args[0], element_id=args[2]);
            else:
                return {"Error": "Insufficient Parameters"};
        elif args[0] == 'delete':
            if args[2]:
                return self.dispatcher.get(args[0])(action=args[0], element_id=args[2]);
            else:
                return {"Error": "Insufficient Parameters"};
        else:
            return {"Error": "Unknown Error"};

    ### Form Generating Functions
    @abstractmethod
    def getFieldData(self, **kwargs):
        pass;

    @abstractmethod
    def getChoiceData(self):
        pass;

    @abstractmethod
    def grabFormData(self, **kwargs):
        data = {
            "field_data": self.getFieldData(**kwargs),
            "choice_data": self.getChoiceData()
        }
        return data;

    ### Table Generating Functions
    @abstractmethod
    def getTableHeader(self):
        pass;

    @abstractmethod
    def getTableRow(self,content):
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