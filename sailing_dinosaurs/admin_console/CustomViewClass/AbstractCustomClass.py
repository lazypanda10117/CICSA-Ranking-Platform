from abc import ABC, abstractmethod
from ..HelperClass import *
from ..generalFunctions import *

from ..models import *
from ..forms import *

class AbstractCustomClass(ABC):

    def __init__(self, request, base_class, validation_table):
        self.dispatcher = self.setDispatcher();
        self.request = request;
        self.base_class = base_class;
        self.validation_table = validation_table;

    def setDispatcher(self):
        dispatcher = Dispatcher();
        dispatcher.add('add', self.grabFormData);
        dispatcher.add('edit', self.grabFormData);
        dispatcher.add('delete', self.grabFormData);
        dispatcher.add('view', self.grabTableData);
        return dispatcher;

### View Process Functions

    @abstractmethod
    def abstractFormProcess(self, action, **kwargs):
        pass;

    def add(self):
        return self.abstractFormProcess('add');

    def edit(self, id):
        return self.abstractFormProcess('edit', id=id);

    def delete(self, id):
        return self.abstractFormProcess('delete', id=id);

### View Generating Functions

    def grabData(self, *args):
        #args[0] = action, args[1] = form_path, args[2] = element_id
        if args[0] == 'view':
            return self.dispatcher.get(args[0])(form_path = args[1]);
        elif args[0] == 'add':
            return self.dispatcher.get(args[0])(action=args[0], element_id=args[2]);
        if args[0] in {'edit', 'delete'}:
            if args[2]:
                return self.dispatcher.get(args[0])(action=args[0], element_id=args[2]);
            else:
                return {"Error": "Insufficient Parameters"};
        else:
            return {"Error": "Unknown Error"};

    ### Form Generating Functions
    def populateDispatcher(self):
        dispatcher = Dispatcher();
        dispatcher.add('add', False);
        dispatcher.add('edit', True);
        dispatcher.add('delete', True);
        return dispatcher;

    @abstractmethod
    def getFieldData(self, **kwargs):
        pass;

    @abstractmethod
    def getChoiceData(self):
        pass;

    def grabFormData(self, **kwargs):
        data = {
            "field_data": self.getFieldData(**kwargs),
            "choice_data": self.getChoiceData()
        }
        return data;

    ### Table Generating Functions
    def getTableHeader(self):
        return self.getTableSpecificHeader() + ["edit", "delete"];

    @abstractmethod
    def getTableSpecificHeader(self):
        pass;

    def getTableRow(self, content):
        rowContent = {};
        rowContent["db_content"] = self.getTableRowContent(content);
        rowContent["button"] = self.makeEditDeleteBtn('custom', str(content.id));
        return rowContent;

    @abstractmethod
    def getTableRowContent(self, content):
        pass;

    def updateChoiceAsValue(self, field_data, choice_data):
        temp_data = field_data;
        for key, value in choice_data.items():
            temp_data[key] = grabLinkValueFromChoices(value, field_data[key]);
        return temp_data;

    def makeEditDeleteBtn(self, path, id):
        editBtn = Button('Edit', 'info', generateGETURL(path, {"action": 'edit', "element_id": id}));
        deleteBtn = Button('Delete', 'danger', generateGETURL(path, {"action": 'delete', "element_id": id}))
        return [editBtn, deleteBtn];

    def getTableContent(self):
        return [self.getTableRow(content) for content in self.base_class.objects.all()];

    def grabTableData(self, form_path):
        tableHeader = self.getTableHeader();
        tableContent = self.getTableContent();
        table = Table(self.base_class, form_path).makeCustomTables(tableHeader, tableContent);
        return [table];