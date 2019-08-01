from enum import Enum


class ActionType:
    VIEW = 'view'
    ADD = 'add'
    EDIT = 'edit'
    DELETE = 'delete'


class ComponentType:
    PROCESS = 'action_process'
    TABLE = 'table_view'
    FORM = 'form_view'
