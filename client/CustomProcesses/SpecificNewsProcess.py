from django.shortcuts import redirect
from django.urls import reverse

from client.CustomProcesses.GenericClientProcess import GenericClientProcess
from misc.CustomFunctions import RequestFunctions
from api.functional_api import NewsAPI


class SpecificNewsProcess(GenericClientProcess):
    def process(self):
        news_api = NewsAPI(self.request)
        post_dict = dict(self.request.POST)
        action = self.param.get("action", None)
        news_id = RequestFunctions.getSingleRequestObj(post_dict, "id")

        if action == "bump":
            bump_up = True if RequestFunctions.getSingleRequestObj(post_dict, "bump") == "up" else False
            if bump_up:
                news_api.bumpNews(news_id)
            else:
                news_api.unbumpNews(news_id)
        elif action == 'comment':
            comment_content = RequestFunctions.getSingleRequestObj(post_dict, 'comment_content')
            news_api.replyComment(news_id, comment_content)
        else:
            raise Exception("The requested action cannot be resolved in SpecificNewsProcess.")

        return redirect(
            reverse(
                'client.view_dispatch_param',
                args=['specific_news', news_id]
            )
        )

    def parseParams(self, param):
        super().parseMatch('^(bump|comment)$')
        param = dict(
            action=param
        )
        return param
