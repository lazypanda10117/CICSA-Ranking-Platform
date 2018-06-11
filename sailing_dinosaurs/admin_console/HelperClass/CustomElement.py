from ..generalFunctions import *

class Button:
    def __init__(self, title, style, redirect):
        self.title = title;
        self.style = style;
        self.redirect = redirect;

class Table:
    def __init__(self, currentClass, title):
        self.currentClass = currentClass;
        self.title = title;
        self.tableElement = '';
        self.tableHeader = '';
        self.tableContent = '';

    def makeTable(self):
        self.tableElement = self.getTableElement('general');
        self.tableHeader = self.getTableHeader();
        self.tableContent = self.getTableContent();
        return self;

    def makeCustomTables(self, tableHeader, tableContent):
        self.tableElement = self.getTableElement('custom');
        self.tableHeader = tableHeader;
        self.tableContent = tableContent;
        return self;

    def getTableElement(self, process):
        def makeAddBtn(path):
            addBtn = Button('Add', 'success', generateGETURL(path, {"action": 'add'}));
            return dict(add_button=addBtn);
        return makeAddBtn(process);

    def getTableHeader(self):
        fields = [field.name for field in self.currentClass._meta.get_fields()] + ["edit", "delete"];
        return fields;

    def getTableContent(self):
        def makeEditDeleteBtn(path, id):
            editBtn = Button('Edit', 'info', generateGETURL(path, {"action": 'edit', "element_id": id}));
            deleteBtn = Button('Delete', 'danger', generateGETURL(path, {"action": 'delete', "element_id": id}))
            return [editBtn, deleteBtn];

        def getTableRow(content):
            rowContent = {"db_content": list(vars(content).values())[1:],
                          "button": makeEditDeleteBtn('general', str(content.id))};
            return rowContent;

        return [getTableRow(content) for content in self.currentClass.objects.all()];

class Form:
    def __init__(self, form_path, form_name, form_action, destination, form):
        self.form_path = form_path;
        self.form_id = self.getFormID(form_name);
        self.form_action = form_action.title();
        self.destination = destination;
        self.form = form;

    def getFormID(self, form_string):
        return self.form_path + form_string;

class Choices:
    STATUS_CHOICES = (
        ("active", "Active"),
        ("dormant", "Dormant"),
        ("hidden", "Hidden")
    );
    TEAM_STATUS_CHOICES = (
        ("active", "Active"),
        ("dormant", "Dormant"),
        ("hidden", "Hidden")
    );
    REGION_CHOICES = tuple([(value.id, value.region_name) for value in filterModelObject(Region)]);
    SCHOOL_CHOICES = tuple([(value.id, value.school_name) for value in filterModelObject(School)]);
    ACCOUNT_TYPE_CHOICES = (
        ("admin", "Admin"),
        ("school", "School")
    );

