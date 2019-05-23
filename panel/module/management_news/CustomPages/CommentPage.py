from panel.module.base.block.CustomPages import AbstractBasePage
from panel.module.base.block.CustomComponents import BlockObject, BlockSet, PageObject
from api.functional_api import NewsAPI


class CommentPage(AbstractBasePage):
    def getPagePath(self):
        return 'platform/module/management_news/admin_comment.html'

    def generateList(self):
        def genCommentDict(news_id):
            comments = news_api.getCommentsById(news_id).order_by('-news_comment_create_time')
            comment_dict = map(lambda comment: dict(
                comment_id=comment.id,
                # should truncate content for preview
                comment_content=comment.news_comment_content,
                # should get the name here
                comment_owner=comment.news_comment_owner,
                # should get the title here
                comment_post_id=comment.news_comment_post_id,
                comment_create_time=comment.news_comment_create_time,
                comment_delete_btn='<button type="button" class="btn btn-outline-danger" name="deleteBtn{}" '
                                   'onclick="deleteComment({})">Delete</button>'.format(comment.id, comment.id)
            ), [comment for comment in comments])
            return BlockObject(
                "",
                "",
                ["Comment ID", "Comment", "Commented By", "Post ID", "Created Time", "Delete"],
                comment_dict)

        news_id = self.param.get("id", None)
        news_id = None if news_id == 'all' else news_id
        news_api = NewsAPI(self.request)
        return BlockSet().makeBlockSet(genCommentDict(news_id))

    def render(self):
        return super().renderHelper(PageObject('Comment Management', self.generateList(), 'Comments'))

    def parseParams(self, param):
        match = super().parseMatch('(\d+|all)')
        param = dict(id=param)
        return param
