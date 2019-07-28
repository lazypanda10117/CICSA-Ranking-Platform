from enum import Enum


class ActionType(Enum):
    VIEW = 'view'
    ADD = 'add'
    EDIT = 'edit'
    DELETE = 'delete'


class ComponentType(Enum):
    PROCESS = 'action_process'
    TABLE = 'table_view'
    FORM = 'form_view'
