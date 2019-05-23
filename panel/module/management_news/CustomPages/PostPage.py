from panel.module.base.block.CustomPages import AbstractBasePage
from panel.module.base.block.CustomComponents import BlockObject, BlockSet, PageObject
from api.functional_api import NewsAPI
from misc.CustomFunctions import MiscFunctions


class PostPage(AbstractBasePage):
    def getPagePath(self):
        return 'platform/module/management_news/admin_post.html'

    def generateList(self):
        def genPostDict():
            news_posts = news_api.getNews().order_by('-news_post_create_time')
            news_post_dict = map(lambda post: dict(
                news_post_id=post.id,
                news_post_title=MiscFunctions.truncateText(post.news_post_title, 50),
                news_post_content=MiscFunctions.truncateText(post.news_post_content, 50),
                news_post_bumps=post.news_post_bumps,
                news_post_create_time=post.news_post_create_time.strftime("%Y-%m-%d %H:%M:%S"),
                news_post_edit_btn='<button type="button" class="btn btn-outline-info" name="editBtn{{post.id}}" '
                                   'onclick="editPost({{post.id}})">Edit</button>',
                news_post_delete_btn='<button type="button" class="btn btn-outline-danger" name="deleteBtn{{post.id}}" '
                                     'onclick="deletePost({{post.id}})">Delete</button> '
            ), [post for post in news_posts])
            return BlockObject(
                "",
                "",
                ["Post ID", "Title", "Content", "Bumps", "Created Time", "Edit", "Delete"],
                news_post_dict)

        news_api = NewsAPI(self.request)
        return BlockSet().makeBlockSet(genPostDict())

    def render(self):
        print(list(self.generateList().blocks[0].contents)[0])
        return super().renderHelper(PageObject('Post Management', self.generateList(), 'All Posts'))

    def parseParams(self, param):
        match = super().parseMatch('')
        param = None
        return param
