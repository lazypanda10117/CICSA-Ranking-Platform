from api.authentication.services.base import BaseService


class ArchiveService(BaseService):
    def __isArchived(self, obj):
        return obj.__archivable__ and obj.archived

    def __filterArchived(self, objects):
        return [o for o in objects if not self.__isArchived(o)]

    # Don't need here if default behavior?
    def _verifyADD(self):
        # return self.__filterArchived(self.objects)
        return self.objects

    def _verifyEDIT(self):
        # Don't allow editing of archived objects
        return self.__filterArchived(self.objects)

    def _verifyDELETE(self):
        # return self.__filterArchived(self.objects)
        return self.objects

    def _verifyVIEW(self):
        return self.objects
