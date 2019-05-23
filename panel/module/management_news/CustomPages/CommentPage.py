from panel.module.base.block.CustomPages import AbstractBasePage
from panel.module.base.block.CustomComponents import BlockObject, BlockSet, PageObject
from api.functional_api import NewsAPI


class PostPage(AbstractBasePage):
    def getPagePath(self):
        return 'platform/module/management_news/admin_comment.html'

    def generateList(self):
        def genCommentDict(news_id):
            comments = news_api.getComments(news_id).order_by('-news_post_create_time')
            comment_dict = map(lambda comment: dict(
                comment_id=comment.id,
                # should get the name here
                comment_owner=comment.news_comment_owner,
                # should get the title here
                comment_post_id=comment.news_comment_post_id,
                # should truncate content for preview
                comment_content=comment.news_comment_content,
                comment_create_time=comment.news_comment_create_time
            ), [comment for comment in comments])
            return BlockObject('Comments', 'Comment', [], comment_dict)

        news_id = self.param.get("id", None)
        news_api = NewsAPI(self.request)
        return BlockSet().makeBlockSet(genCommentDict(news_id))

    def render(self):
        return super().renderHelper(PageObject('Comment Management', self.generateList(), []))

    def parseParams(self, param):
        match = super().parseMatch('\d+')
        param = dict(id=param)
        return param
