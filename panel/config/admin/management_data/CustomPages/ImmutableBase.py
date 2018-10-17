import json
from abc import ABC, abstractmethod
from panel.component.CustomElements import Table
from misc.CustomElements import Dispatcher
from misc.CustomFunctions import APIFunctions, MiscFunctions, RequestFunctions


class ImmutableBase(ABC):
    def __init__(self, request, base_class, validation_table):
        self.dispatcher = self.setViewDispatcher()
        self.request = request
        self.base_class = base_class
        self.api_table = self.setAPIDispatcher()
        self.validation_table = validation_table

    @staticmethod
    def setAPIDispatcher():
        dispatcher = APIFunctions.getModelAPIDispatcher()
        return dispatcher

    @staticmethod
    def setViewDispatcher():
        dispatcher = Dispatcher()
        dispatcher.add('add', True)
        dispatcher.add('edit', False)
        dispatcher.add('delete', False)
        dispatcher.add('view', True)
        return dispatcher

    @staticmethod
    def serializeJSONListData(tags, data):
        to_serialize = tags
        for json_obj_ref in to_serialize:
            if json_obj_ref in data:
                data[json_obj_ref] = json.dumps(data[json_obj_ref])
        return data

    def getFilterTerms(self):
        get_dict = self.request.GET
        kwargs = RequestFunctions.getMultiplePostObj(get_dict, 'kwargs')
        if kwargs is not None:
            kwargs = json.loads(kwargs)
            return kwargs
        return {}

    def getRangeTerms(self):
        get_dict = self.request.GET
        range_start = RequestFunctions.getMultiplePostObj(get_dict, 'start')
        range_end = RequestFunctions.getMultiplePostObj(get_dict, 'end')

        try:
            range_start = (int(range_start)-1 if int(range_start)-1 >= 0 else 0)
        except Exception:
            range_start = 0

        try:
            range_end = (int(range_end) if int(range_end) >= 0 else 0)
        except Exception:
            range_end = 0

        if range_end <= range_start:
            range_start = 0
            range_end = None

        return range_start, range_end

    # View Process Functions
    @abstractmethod
    def abstractFormProcess(self, action, **kwargs):
        pass

    def add(self):
        return self.abstractFormProcess('add')

    def edit(self, edit_id):
        return self.abstractFormProcess('edit', id=edit_id)

    def delete(self, delete_id):
        return self.abstractFormProcess('delete', id=delete_id)

# View Generating Functions

    def grabData(self, *args):
        # args[0] = action, args[1] = form_path, args[2] = element_id
        if args[0] == 'view':
            return self.grabTableData(form_path=args[1])
        elif args[0] == 'add':
            return self.grabFormData(action=args[0], element_id=args[2])
        if args[0] in {'edit', 'delete'}:
            if args[2]:
                return self.grabFormData(action=args[0], element_id=args[2])
            else:
                return {"Error": "Insufficient Parameters"}
        else:
            return {"Error": "Unknown Error"}

    # Form Generating Functions
    @staticmethod
    def populateDispatcher():
        dispatcher = Dispatcher()
        dispatcher.add('add', False)
        dispatcher.add('edit', True)
        dispatcher.add('delete', True)
        return dispatcher

    @abstractmethod
    def getFieldData(self, **kwargs):
        pass

    @abstractmethod
    def getChoiceData(self):
        pass

    @abstractmethod
    def getDBMap(self, data):
        pass

    @abstractmethod
    def getMultiChoiceData(self):
        pass

    @abstractmethod
    def getSearchElement(self, **kwargs):
        pass

    def grabFormData(self, **kwargs):
        data = {
            "field_data": self.getFieldData(**kwargs),
            "choice_data": self.getChoiceData(),
            "multi_choice_data": self.getMultiChoiceData()
        }
        special_field = {
            "search": self.getSearchElement(**kwargs)
        }
        return {"data": data, "special_field": special_field}

    # Table Generating Functions
    def getTableHeader(self):
        return self.getTableSpecificHeader()

    @abstractmethod
    def getTableSpecificHeader(self):
        pass

    def getTableRow(self, content):
        rowContent = dict()
        rowContent["db_content"] = self.getTableRowContent(content)
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
                self.useAPI(self.base_class).filterSelf(**kwargs),
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

    def grabTableData(self, form_path):
        tableHeader = self.getTableHeader()
        tableContent = self.getTableContent(self.getRangeTerms(), **self.getFilterTerms())
        table = Table(self.base_class, form_path).makeCustomTables(tableHeader, tableContent)
        return [table]

# Useful Functions
    def useAPI(self, model):
        return self.api_table.get(MiscFunctions.getModelName(model))(self.request)
