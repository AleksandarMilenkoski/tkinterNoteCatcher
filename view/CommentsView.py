import config
from tkinter import Tk, PhotoImage, Frame, BOTH, GROOVE, TRUE, X, Y, Menu, LEFT, StringVar, N, W, NW, TOP, RIGHT, \
    NE, FLAT
from tkinter.ttk import Label, Entry, Button
from view.additionaltkinterelements.ScrolledFrame import ScrolledFrame
from view.additionaltkinterelements.ScrolledText import ScrolledText

class CommentsView:
    '''
    CommentsView class
    '''



    def __init__(self, controller):
        self.controller = controller
        self.main()

    def main(self):
        # root window
        self.root = Tk()
        # window setup
        self._set_main_window_title()
        self._set_main_window_dimensions()
        # self._position_main_window()
        self._set_main_window_fav_icon()
        self._set_main_menu()
        self._set_main_window_layout()
        self._render_search_bar()
        self.update_comments()
        # main loop window
        self.root.mainloop()

    def _set_main_window_title(self):
        self.root.title(config.WINDOW_TITLE)

    def _set_main_window_dimensions(self):
        pass

    def _position_main_window(self):
        self.root.update()
        screen_height = self.root.winfo_screenheight()
        screen_width = self.root.winfo_screenwidth()
        window_height = self.root.winfo_height()
        window_width = self.root.winfo_width()
        self.root.geometry('{}x{}+{}+{}'.format(window_width,
                                                window_height,
                                                int((screen_width - window_width) / 2),
                                                int((screen_height - window_height) / 2)))

    def _set_main_window_fav_icon(self):
        self.root.tk.call('wm', 'iconphoto', self.root._w, PhotoImage(file=config.ICON_FILE))

    def _set_main_menu(self):
        main_menu = Menu(self.root)

        main_menu.add_command(label = 'Add Comment')

        self.root.config(menu = main_menu)

    def _set_main_window_layout(self):
        main_frame = Frame(self.root)
        # main_frame.config(bg = 'white')
        main_frame.pack(fill='both', expand=True)

        self._search_frame = search_frame = Frame(main_frame, bg='red')
        search_frame.pack()
        # search_frame.config(bg='red')

        self._comments_frame = comments_frame = Frame(main_frame, borderwidth=5)
        comments_frame.pack(side=TOP, anchor=N, ipadx=10, ipady=10, padx=10, pady=10, fill=BOTH, expand=True)

        self._pagination_frame = pagination_frame = Frame(main_frame, bg='orange')
        pagination_frame.pack(side=TOP, anchor=N, ipadx=10, ipady=10, padx=10, pady=10)

    def _render_search_bar(self):
        self._serach_value = serach_value = StringVar()

        search_container = Frame(self._search_frame, bg='brown')
        search_container.pack(side=TOP, anchor=N, padx=10, pady=10)

        Label(search_container, text=config.SEARCH_LABEL_TEXT).pack(side=LEFT)

        Entry(search_container, textvariable=serach_value, width=30).pack(side=LEFT)

        Button(search_container, text='Search').pack(side=LEFT)

        Button(search_container, text='Clear').pack(side=LEFT)

    @staticmethod
    def _clearElementChilderns(element):
        for widget in element.winfo_children():
            widget.destroy()

    def update_comments(self):
        outer_comments_container = ScrolledFrame(self._comments_frame)
        outer_comments_container.pack(fill=BOTH, expand=True)
        inner_comments_container = Frame(outer_comments_container)
        inner_comments_container.pack(ipadx=10)
        # tmp_cont = Frame(inner_comments_container, bg='red')
        # tmp_cont.pack(padx=10, pady=10, ipadx=10, ipady=10)
        # comments_container.config(width=800)
        # comments_container.grid_propagate(0)
        for i in range(0, 5):
            self._render_comment(i, inner_comments_container)

        outer_comments_container.update_scroll_bars()
        # print(comments_container.winfo_width())

    def _render_comment(self, row, parent):
        comment_container = Frame(parent)
        comment_container.pack()

        text_conainer = Frame(comment_container)
        text_conainer.pack(side=LEFT)

        text = ScrolledText(text_conainer)
        text.pack()
        text.config(width=50, height=10)

        stretched_space = Frame(comment_container)
        stretched_space.pack(side=LEFT, fill='both', expand=True, padx=10, ipadx=10)

        buttons_conainer = Frame(comment_container)
        buttons_conainer.pack(side=RIGHT, pady=5, anchor=NE)

        edit_button = Button(buttons_conainer, text='Edit')
        edit_button.grid(row=0, column=0)

        delete_button = Button(buttons_conainer, text='Delete')
        delete_button.grid(row=0, column=1)

        copy_button = Button(buttons_conainer, text='Copy')
        copy_button.grid(row=1, column=0)

        save_button = Button(buttons_conainer, text='Save')
        save_button.grid(row=0, column=2)

        cancel_button = Button(buttons_conainer, text='Cancel')
        cancel_button.grid(row=1, column=2)



