from blackbox.block_app.management_event.views import ManagementEventView as MEView


class ManagementEventView(MEView):
    def home(self, request):
        return super().home(request);