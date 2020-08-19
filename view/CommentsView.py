from tkinter import Tk
from tkinter.ttk import Frame
# from controller.CommentsController import CommentsController

class CommentsView:
    '''
    CommentsView class
    '''

    def __init__(self, controller):
        self.controller = controller
        self.main()

    def main(self):
        self.root = Tk()
        self.root.mainloop()
