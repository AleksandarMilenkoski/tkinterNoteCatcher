from tkinter import Tk
from tkinter.ttk import Frame

class CommentsView:
    '''
    CommentsView class
    '''

    TITLE = 'Comments App'

    def __init__(self, controller):
        self.controller = controller
        self.main()

    def main(self):
        self.root = Tk()

        self._set_main_window_title()
        self._set_main_window_dimensions()
        self._position_main_window()

        self.root.mainloop()

    def _set_main_window_title(self):
        self.root.title(CommentsView.TITLE)

    def _set_main_window_dimensions(self):
        pass

    def _position_main_window(self):
        self.root.update()
        screenHeight = self.root.winfo_screenheight()
        screenWidth = self.root.winfo_screenwidth()
        windowHeight = self.root.winfo_height()
        windowWidth = self.root.winfo_width()
        self.root.geometry('{}x{}+{}+{}'.format(windowWidth,
                                                windowHeight,
                                                int((screenWidth - windowWidth) / 2),
                                                int((screenHeight - windowHeight) / 2 )))
