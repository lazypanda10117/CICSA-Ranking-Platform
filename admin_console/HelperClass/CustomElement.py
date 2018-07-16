from ..generalFunctions import *

class Button:
    def __init__(self, title, style, redirect):
        self.title = title;
        self.style = style;
        self.redirect = redirect;

class FieldExtendButton:
    def __init__(self):
        pass;

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

        return [getTableRow(content) for content in sorted(self.currentClass.objects.all(), key=lambda q: q.id)];

class Form:
    def __init__(self, form_path, form_name, form_action, destination, form):
        self.form_path = form_path;
        self.form_id = self.getFormID(form_name);
        self.form_action = form_action.title();
        self.destination = destination;
        self.form = form;

    def getFormID(self, form_string):
        return form_string+self.form_path;

class SearchElement:
    #name = search base name
    #label = the text to display for the search box
    #item = the class to search for
    #key = unknown
    #term = the kwargs to search for
    #help term = an extra to display in the search dropdown to help further distinguish between results

    def __init__(self, name, label, item, key, term, help_term, value_tuple):
        self.name = name;
        self.label = label;
        self.item = self.stringify(item);
        self.key = self.stringify(key);
        self.term = self.stringify(term);
        self.help_term = self.stringify(help_term);
        self.default_value = value_tuple[0];
        self.value = value_tuple[1];

    def stringify(self, text):
        return "'" + text + "'";


class Choices:
    def getSeasonChoices(self):
        SEASON_CHOICES = tuple([(value.id, value.season_name) for value in filterModelObject(Season)]);
        return SEASON_CHOICES;

    def getRegionChoices(self):
        REGION_CHOICES = tuple([(value.id, value.region_name) for value in filterModelObject(Region)]);
        return REGION_CHOICES;

    def getSchoolChoices(self):
        SCHOOL_CHOICES = tuple([(value.id, value.school_name) for value in filterModelObject(School)]);
        return SCHOOL_CHOICES;

    def getEventTypeChoices(self):
        EVENT_TYPE_CHOICES = tuple([(value.id, value.event_type_name) for value in filterModelObject(EventType)]);
        return EVENT_TYPE_CHOICES;

    def getEventStatusChoices(self):
        EVENT_STATUS_CHOICES = (
            ("future", "Future"),
            ("done", "Done"),
            ("running", "Running")
        );
        return EVENT_STATUS_CHOICES;

    def getEventActivityTypeChoices(self):
        EVENT_ACTIVITY_TYPE_CHOICES = (
            ("race", "Race"),
            ("other", "Other")
        );
        return EVENT_ACTIVITY_TYPE_CHOICES;

    def getTeamStatusChoices(self):
        TEAM_STATUS_CHOICES = (
            ("active", "Active"),
            ("dormant", "Dormant"),
            ("hidden", "Hidden")
        );
        return TEAM_STATUS_CHOICES;

    def getStatusChoices(self):
        STATUS_CHOICES = (
            ("active", "Active"),
            ("dormant", "Dormant"),
            ("hidden", "Hidden")
        );
        return STATUS_CHOICES;

    def getAccountTypeChocies(self):
        ACCOUNT_TYPE_CHOICES = (
            ("admin", "Admin"),
            ("school", "School")
        );
        return ACCOUNT_TYPE_CHOICES;

class DBMap():
    def getMap(self, query_class, query_id, target_field):
        return noneCatcher(target_field, getModelObject(query_class, id=query_id).__dict__);