from view.CommentsView import CommentsView
from model.CommentsModel import CommentsModel


class CommentsController:
    '''
    CommentsController class
    '''

    def __init__(self):
        self.view = CommentsView(self)
        self.model = CommentsModel()



if __name__ == '__main__':
    CommentsController()
