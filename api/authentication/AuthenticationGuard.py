from misc.CustomFunctions import AuthFunctions
from api.authentication import AuthenticationType
from api.authentication import AuthenticationGuardType


class AuthenticationGuard:
	def __init__(self, permission, request, context=None):
		self.request = request
		self.context = context
		self.permission = permission
  
  # Prev conflict: has callback=None as parameter
	def guard(self, api=True, **kwargs):
		if self.permission == AuthenticationGuardType.ADMIN_GUARD:
			allowed_types = [AuthenticationType.ADMIN]
		elif self.permission == AuthenticationGuardType.TEAM_GUARD:
			allowed_types = [AuthenticationType.TEAM]
		elif self.permission == AuthenticationGuardType.PUBLIC_GUARD:
			allowed_types = [AuthenticationType.PUBLIC, AuthenticationType.TEAM, AuthenticationType.ADMIN]
		elif self.permission == AuthenticationGuardType.ADMIN_TEAM_GUARD:
			allowed_types = [AuthenticationType.ADMIN, AuthenticationType.TEAM]
		elif self.permission == AuthenticationGuardType.LOGIN_GUARD:
			allowed_types = [AuthenticationType.ADMIN, AuthenticationType.TEAM]
		elif self.permission == AuthenticationGuardType.NO_GUARD:
			allowed_types = [AuthenticationType.PUBLIC, AuthenticationType.ADMIN, AuthenticationType.TEAM]
		else:
			raise Exception("Failed Authentication Process During AuthenticationGuard Stage")

		return AuthFunctions.kickRequest(
			request=self.request,
			api=api,
			allowed_types=allowed_types,
			**kwargs
		)
