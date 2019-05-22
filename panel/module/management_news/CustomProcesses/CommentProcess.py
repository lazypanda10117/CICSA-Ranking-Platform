from django.shortcuts import redirect, reverse
from misc.CustomFunctions import RequestFunctions
from panel.module.base.block.CustomProcesses import AbstractBaseProcess
from api.functional_api.NewsAPI import NewsAPI


class CommentProcess(AbstractBaseProcess):
    def process(self):
        news_api = NewsAPI(self.request)
        post_dict = dict(self.request.POST)
        action = self.param.get("action", None)
        comment_id = RequestFunctions.getSinglePostObj(post_dict, "id")

        if action == 'delete':
            news_api.deleteComment(comment_id)

        return redirect(
            reverse(
                'panel.module.management_news.view_dispatch',
                args=['comment']
            )
        )

    def parseParams(self, param):
        match = super().parseMatch('(add|edit|delete)')
        param = dict(
            action=param
        )
        return param