from abc import ABC, abstractmethod

from api.authentication import AuthenticationActionType
from api.authentication.base.AuthenticationSizeAuthenticate import AuthenticationSizeAuthenticate
from misc.CustomElements import Dispatcher


class AuthenticationComponentBase(ABC):    
	def __init__(self, request):
		self.request = request
		self.base = self.setBaseModelClass()

	@abstractmethod
	def setBaseModelClass(self):
		pass

	# This is only being called when passed in a none object. 
	# Essentially does nothing, just for completeness sake.
	class NoneAuthenticate(AuthenticationSizeAuthenticate):
		def viewAuthenticate(self):
			return []

		def editAuthenticate(self):
			return []

		def addAuthenticate(self):
			return []

		def deleteAuthenticate(self):
			return []

	# This is called when you pass in a bulk object
	class BulkAuthenticate(AuthenticationSizeAuthenticate):
		def viewAuthenticate(self):
			return list(self.objects)

		def editAuthenticate(self):
			return list(self.objects)

		def addAuthenticate(self):
			return list(self.objects)

		def deleteAuthenticate(self):
			return list(self.objects)

	class SingleAuthenticate(AuthenticationSizeAuthenticate):
		def viewAuthenticate(self):
			return [self.objects]

		def editAuthenticate(self):
			return [self.objects]

		def addAuthenticate(self):
			return [self.objects]

		def deleteAuthenticate(self):
			return [self.objects]

	# Passing in query objects, and returning objects of same type through return transformer
	def authTypeDispatcher(self, objects):
		if objects is None:
			return self.NoneAuthenticate(self.request, objects)
		elif type(objects) == 'QuerySet':
			return self.BulkAuthenticate(self.request, objects)
		else:
			return self.SingleAuthenticate(self.request, objects)

	def getAuthDispatcher(self, objects):
		dispatcher = Dispatcher()
		dispatcher.add(
			AuthenticationActionType.VIEW, 
			self.authTypeDispatcher(objects).rootAuthenticate(AuthenticationActionType.VIEW)
		)
		dispatcher.add(
			AuthenticationActionType.ADD, 
			self.authTypeDispatcher(objects).rootAuthenticate(AuthenticationActionType.ADD)
		)
		dispatcher.add(
			AuthenticationActionType.EDIT, 
			self.authTypeDispatcher(objects).rootAuthenticate(AuthenticationActionType.EDIT)
		)
		dispatcher.add(
			AuthenticationActionType.DELETE, 
			self.authTypeDispatcher(objects).rootAuthenticate(AuthenticationActionType.DELETE)
		)
		return dispatcher

	def authenticate(self, route, objects):
		return self.getAuthDispatcher(objects).get(route)
