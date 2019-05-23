from panel.module.base.block.CustomPages import AbstractBasePage
from panel.module.base.block.CustomComponents import BlockObject, BlockSet, PageObject
from api.functional_api import NewsAPI


class PostPage(AbstractBasePage):
    def getPagePath(self):
        return 'platform/module/management_news/admin_post.html'

    def generateList(self):
        def genPostDict():
            news_posts = news_api.getAllNews().order_by('-news_post_create_time')
            news_post_dict = map(lambda post: dict(
                news_post_id=post.id,
                news_post_title=post.news_post_title,
                news_post_content=post.news_post_content,
                news_post_bumps=post.news_post_bumps,
                news_post_created_time=post.news_post_created_time
            ), [post for post in news_posts])
            return BlockObject('Posts', 'Post', [], news_post_dict)

        news_api = NewsAPI(self.request)
        return BlockSet().makeBlockSet(genPostDict())

    def render(self):
        return super().renderHelper(PageObject('Post Management', self.generateList(), []))

    def parseParams(self, param):
        match = super().parseMatch('')
        param = None
        return param
