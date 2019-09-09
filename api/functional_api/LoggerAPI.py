from api.authentication import AuthenticationGuardType
from api.base import AbstractCoreAPI
from api.model_api import LogAPI


class LoggerAPI(AbstractCoreAPI):
    def __init__(self, request):
        super().__init__(request=request, permission=AuthenticationGuardType.ADMIN_GUARD)

    def pruneLog(self):
        result = LogAPI(self.request).getAll()
        result.delete()
