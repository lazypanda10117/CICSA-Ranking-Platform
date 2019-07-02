from enum import Enum


class AuthenticationGuardType(Enum):
	ADMIN_GUARD = 1
	TEAM_GUARD = 2
	PUBLIC_GUARD = 3
	ADMIN_TEAM_GUARD = 4
	LOGIN_GUARD = 5


class AuthenticationType:
	ADMIN = "admin"
	TEAM = "team"
	PUBLIC = "public"


class AuthenticationActionType:
	ADD = 'add'
	EDIT = 'edit'
	DELETE = 'delete'
	VIEW = 'view'
