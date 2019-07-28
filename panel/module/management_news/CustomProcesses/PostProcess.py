from django.shortcuts import redirect, reverse
from misc.CustomFunctions import RequestFunctions
from panel.module.base.block.CustomProcesses import AbstractBaseProcess
from api.functional_api.NewsAPI import NewsAPI


class PostProcess(AbstractBaseProcess):
    def process(self):
        news_api = NewsAPI(self.request)
        post_dict = dict(self.request.POST)
        action = self.param.get("action", None)
        news_id = RequestFunctions.getSingleRequestObj(post_dict, "id")

        if action == 'add':
            news_title = RequestFunctions.getSingleRequestObj(post_dict, 'news_title')
            news_content = RequestFunctions.getSingleRequestObj(post_dict, 'news_content')
            news_api.addNews(news_title, news_content)
        elif action == 'edit':
            news_title = RequestFunctions.getSingleRequestObj(post_dict, 'news_title')
            news_content = RequestFunctions.getSingleRequestObj(post_dict, 'news_content')
            news_api.editNews(news_id, news_title, news_content)
        elif action == 'delete':
            news_api.deleteNews(news_id)

        return redirect(
            reverse(
                'panel.module.management_news.view_dispatch',
                args=['post']
            )
        )

    def parseParams(self, param):
        super().parseMatch('(add|edit|delete)')
        param = dict(
            action=param
        )
        return param
