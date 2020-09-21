from model.gateway.CommentsGateway import CommentsGateway
from model.table.CommentsTable import CommentsTable
import config

class CommentsModel:
    # def __init__(self):
    #     pass

    def get_comments_by_limit_order_by(self, limit, order, current_page):
        response = {}

        response['comments'] = CommentsGateway().getCommentsByLimitOrderby(limit, order, current_page)
        response['comments_count'] = CommentsTable().selectAllCommentsCount()

        return response



if __name__ == '__main__':
    comments_model = CommentsModel()
    comments_model.get_comments_by_limit_order_by(config.COMMENTS_PER_PAGE, config.ORDER_BY, 1)
