from abc import ABC
from abc import abstractmethod

from api.authentication import AuthenticationActionType
from api.authentication.services import ArchiveService
from misc.CustomElements import Dispatcher


class AuthenticationSizeAuthenticate(ABC):
	def __init__(self, request, objects):
		self.request = request
		self.objects = objects
		self.dispatcher = self.__setDispatcher()
		self.authentication_services = [ArchiveService]

	def __setDispatcher(self):
		dispatcher = Dispatcher()
		dispatcher.add(AuthenticationActionType.VIEW, self.viewAuthenticate())
		dispatcher.add(AuthenticationActionType.ADD, self.addAuthenticate())
		dispatcher.add(AuthenticationActionType.EDIT, self.editAuthenticate())
		dispatcher.add(AuthenticationActionType.DELETE, self.deleteAuthenticate())
		return dispatcher

	def __makeQuerySet(self, objects):
		obj_class = objects[0].__class__
		return obj_class.objects.filter(id__in=[o.id for o in objects])

	def _returnTransformer(self, objects):
		if len(objects) == 0:
			return None
		elif len(objects) == 1:
			return objects[0]
		else:
			return self.__makeQuerySet(objects)

	def rootAuthenticate(self, identifier):
		# Probably can use reduce here instead (more functional ;) )
		for auth_service in self.authentication_services:
			self.objects = self._returnTransformer(
				auth_service(self.request, self.objects).verify(identifier)
			)
		return self._returnTransformer(self.dispatcher.get(identifier))

	# Each of these authenticate method takes in a query object (or None) and returns an array of objects
	@abstractmethod
	def viewAuthenticate(self):
		pass

	@abstractmethod
	def editAuthenticate(self):
		pass

	@abstractmethod
	def addAuthenticate(self):
		pass

	@abstractmethod
	def deleteAuthenticate(self):
		pass
