from blackbox.api import SearchAPI


class SearchView():
    def search(self, request):
        item = request.GET.get("item");
        key = request.GET.get("key");
        term = request.GET.get("term");
        return SearchAPI(request).search(item, key, term);