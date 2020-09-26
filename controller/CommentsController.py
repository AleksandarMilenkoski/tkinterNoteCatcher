from view.CommentsView import CommentsView
from model.CommentsModel import CommentsModel
import config
from math import ceil


class CommentsController:
    """
    CommentsController class
    """

    def __init__(self):
        self._view = CommentsView(self)
        self._model = CommentsModel()
        self.get_comments()

    def get_comments(self):
        if not self._check_if_search_phrase_exists():
            self._get_comments_by_limit_order_by()
        else:
            self._get_comments_by_limit_and_phrase_oreder_by()

    def add_comment(self, text):
        self._model.add_comment(text)
        self.get_comments()

    def edit_comment(self, comment):
        # print(comment)
        self._model.edit_comment(comment)
        self.get_comments()

    def delete_comment(self, comment):
        self._model.delete_comment(comment)

        self._check_last_current_comments_page()

        self.get_comments()

    def get_view(self):
        return self._view

    def _get_comments_by_limit_and_phrase_oreder_by(self):
        # print('Search Phrase ' + self._view.serarch_phrase)
        response = self._model.get_comments_by_limit_and_phrase_oreder_by(self._view.serarch_phrase,
                                                                          config.COMMENTS_PER_PAGE,
                                                                          config.ORDER_BY, self._view.current_page)
        # print(response)

        self._view.comments_count = response['comments_count']
        self._view.update_coments_with_search_phrase(response['comments'])

    def _get_comments_by_limit_order_by(self):
        response = self._model.get_comments_by_limit_order_by(config.COMMENTS_PER_PAGE,
                                                              config.ORDER_BY, self._view.current_page)

        self._view.comments_count = response['comments_count']
        self._view.update_comments(response['comments'])

    def _check_last_current_comments_page(self):
        # search_phrase = self._view.serarch_phrase
        comments_count = 0
        if not self._check_if_search_phrase_exists():
            comments_count = self._model.get_all_comments_count()
        else:
            comments_count = self._model.get_comments_by_phrase_count(self._view.serarch_phrase)

        total_pages = ceil(comments_count / config.COMMENTS_PER_PAGE)
        if self._view.current_page > total_pages:
            if total_pages == 0:
                self._view.current_page = 1
            else:
                self._view.current_page = total_pages

    def _check_if_search_phrase_exists(self):
        if self._view.serarch_phrase == '':
            return False
        return True

# if __name__ == '__main__':
#     CommentsController()
