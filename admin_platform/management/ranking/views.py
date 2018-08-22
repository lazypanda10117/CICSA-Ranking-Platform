from blackbox.block_app.management_ranking.views import ManagementRankingView as MRView


class ManagementEventView(MRView):
    def home(self, request):
        return super().home(request);