from .Login import Login


class PermissionView():
    def __init__(self):
        self.permission_object = Login;

    def login(self, request):
        return self.permission_object(request).login();

    def logout(self, request):
        return self.permission_object(request).logout();