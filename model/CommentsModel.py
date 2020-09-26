from model.gateway.CommentsGateway import CommentsGateway
from model.table.CommentsTable import CommentsTable
import config

class CommentsModel:
    # def __init__(self):
    #     pass

    def get_comments_by_limit_order_by(self, limit, order, current_page):
        response = {}

        response['comments'] = CommentsGateway().getCommentsByLimitOrderby(limit, order, current_page)
        response['comments_count'] = self.get_all_comments_count()

        return response

    def get_comments_by_limit_and_phrase_oreder_by(self, phrase, limit, order, current_page):
        response = {}

        # print('in model')

        response['comments'] = CommentsGateway().getCommentByPhraseLimitOrder(phrase, limit, order, current_page)
        response['comments_count'] = self.get_comments_by_phrase_count(phrase)
        # print(response)

        return response

    def get_all_comments_count(self):
        return CommentsTable().selectAllCommentsCount()

    def get_comments_by_phrase_count(self, phrase):
        return CommentsTable().selectCommentsByPhraseCount(phrase)

    def add_comment(self, text):
        CommentsTable().InsertComment(text)

    def edit_comment(self, comment):
        # print(comment)
        CommentsGateway().editComment(comment)

    def delete_comment(self, comment):
        # print(comment.get_id())
        CommentsGateway().deleteComment(comment)



if __name__ == '__main__':
    comments_model = CommentsModel()
    comments_model.get_comments_by_limit_order_by(config.COMMENTS_PER_PAGE, config.ORDER_BY, 1)
