from view.CommentsView import CommentsView
from model.CommentsModel import CommentsModel
import config


class CommentsController:
    """
    CommentsController class
    """

    def __init__(self):
        self._view = CommentsView(self)
        self._model = CommentsModel()
        self.get_comments()

    def get_comments(self):
        if self._view.serarch_phrase == '':
            self._get_comments_by_limit_order_by()
        else:
            self._get_comments_by_limit_and_phrase_oreder_by()

    def _get_comments_by_limit_and_phrase_oreder_by(self):
        pass

    def _get_comments_by_limit_order_by(self):
        response = self._model.get_comments_by_limit_order_by(config.COMMENTS_PER_PAGE,
                                                              config.ORDER_BY, self._view.current_page)

        self._view.comments_count = response['comments_count']
        self._view.update_comments(response['comments'])

    def get_view(self):
        return self._view


# if __name__ == '__main__':
#     CommentsController()
