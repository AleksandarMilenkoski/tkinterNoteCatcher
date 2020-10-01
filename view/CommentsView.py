import config
from tkinter import Tk, PhotoImage, Frame, BOTH, GROOVE, TRUE, X, Y, Menu, LEFT, StringVar, N, W, NW, TOP, RIGHT, \
    NE, FLAT, DISABLED, NORMAL, Toplevel, END
from tkinter.ttk import Label, Entry, Button
from view.additionaltkinterelements.ScrolledFrame import ScrolledFrame, ALIGN_CENTER, ALIGN_RIGHT
from view.additionaltkinterelements.TkComment import TkComment
from view.helpers.paginator.PaginatorWithCombobox import PaginatorWithCombobox, pagination_style
from math import ceil
from view.additionaltkinterelements.ScrolledText import ScrolledText

# WINDOW_WIDTH = 840
# WINDOW_HEIGHT = 465


class CommentsView:
    """
    CommentsView class
    """

    def __init__(self, controller):
        self._controller = controller
        self._tk_comments = []
        self.current_page = 1
        self.comments_count = 0
        self.serarch_phrase = ''
        self.main()

    def main(self):
        # root window
        self._root = Tk()

        # print(self.root.cget('bg'))
        # window setup
        self._set_main_window_title()
        self._set_main_window_dimensions()
        self._position_main_window()
        self._set_main_window_fav_icon()
        self._set_main_menu()
        self._set_main_window_layout()
        self._render_search_bar()
        # self._render_comments()
        # self._update_comments()
        self._render_pagination_bar()

        # self._set_main_window_layout_min_size()

        # main loop window
        # self.root.mainloop()

    def main_loop(self):
        self._root.mainloop()

    def _set_main_window_title(self):
        self._root.title(config.WINDOW_TITLE)

    def _set_main_window_dimensions(self):
        pass

    def _position_main_window(self):
        root = self._root
        root.update()
        screen_height = self._root.winfo_screenheight()
        screen_width = self._root.winfo_screenwidth()
        # window_height = self._root.winfo_height()
        window_height = config.WINDOW_HEIGHT
        # window_width = self._root.winfo_width()
        window_width = config.WINDOW_WIDTH
        root.geometry('{}x{}+{}+{}'.format(window_width,
                                                 window_height,
                                                 int((screen_width - window_width) / 2),
                                                 int((screen_height - window_height) / 2)))

        root.minsize(window_width, window_height)

    def _set_main_window_fav_icon(self):
        self._root.tk.call('wm', 'iconphoto', self._root._w, PhotoImage(file=config.ICON_FILE))

    def _set_main_menu(self):
        self._main_menu = main_menu = Menu(self._root)

        main_menu.add_command(label = 'Add Comment', command=self._on_add_button_click)

        self._root.config(menu = main_menu)

    def _set_main_window_layout(self):
        main_frame = Frame(self._root)
        # main_frame.config(bg = 'white')
        main_frame.pack(fill='both', expand=True, pady=(0, 20))

        self._search_frame = search_frame = Frame(main_frame)
        search_frame.pack()
        # search_frame.config(bg='red')

        comments_outer_frame = Frame(main_frame, borderwidth=5)
        comments_outer_frame.pack(side=TOP, anchor=N, ipadx=10, ipady=10, padx=10, pady=(10, 20), fill=BOTH, expand=True)
        self._comments_scrolled_frame = comments_scrolled_frame = ScrolledFrame(comments_outer_frame, ALIGN_CENTER)
        comments_scrolled_frame.pack(fill=BOTH, expand=True)
        self._comments_inner_frame = comments_inner_frame = Frame(comments_scrolled_frame)
        # comments_inner_frame.config( bg='green')
        comments_inner_frame.pack(padx=10, pady=10)

        self._pagination_frame = pagination_frame = Frame(main_frame)
        # pagination_frame.pack(side=TOP, anchor=N, ipadx=10, ipady=10, padx=10, pady=10)
        pagination_frame.pack()

    def _render_search_bar(self):
        serach_value = StringVar()

        def _check_if_empty_search_phrase():
            search_phrase = serach_value.get()
            if search_phrase.strip(' ') == '':
                return ''

            return search_phrase

        def _on_search_button_click():
            search_phrase = _check_if_empty_search_phrase()
            if search_phrase == '':
                return 'break'
            self.serarch_phrase = search_phrase
            self.current_page = 1
            # print(search_phrase)
            self._controller.get_comments()

            return 'break'

        def _on_clear_button_click():
            search_phrase = _check_if_empty_search_phrase()
            if self.serarch_phrase == '':
                return 'break'

            serach_value.set('')
            self.serarch_phrase = ''
            self.current_page = 1
            # print(search_phrase)
            self._controller.get_comments()

            return 'break'

        search_container = Frame(self._search_frame)
        search_container.pack(side=TOP, anchor=N, padx=10, pady=(20,10))

        Label(search_container, text=config.SEARCH_LABEL_TEXT).pack(side=LEFT)

        search_entry = Entry(search_container, textvariable=serach_value, width=30)
        search_entry.pack(side=LEFT, padx=(5, 10))
        search_entry.bind('<Return>', lambda event: _on_search_button_click())
        search_entry.bind('<Escape>', lambda event: _on_clear_button_click())

        Button(search_container, text='Search', command=_on_search_button_click).pack(side=LEFT)

        Button(search_container, text='Clear', command=_on_clear_button_click).pack(side=LEFT)

    def update_coments_with_search_phrase(self, domain_comments_objects):
        self.update_comments(domain_comments_objects)
        for tk_comment in self._tk_comments:
            tk_comment.mark_text(self.serarch_phrase)

    def update_comments(self, domain_commets_objects):
        self._tk_comments = []
        self._clearElementChilderns(self._comments_inner_frame)
        self._render_comments(domain_commets_objects)
        self._paginator.update(ceil(self.comments_count/config.COMMENTS_PER_PAGE), self.current_page)
        self._show_hide_paginator()

    def disable_gui(self):
        self._disable_all_child_elements(self._search_frame)
        self._paginator.disable()
        self._main_menu.entryconfig(1, state=DISABLED)
        for tk_comment in self._tk_comments:
            tk_comment.disable_standard_buttons()

    def enable_gui(self):
        self._enable_all_child_elements(self._search_frame)
        self._paginator.enable()
        self._main_menu.entryconfig(1, state=NORMAL)
        for tk_comment in self._tk_comments:
            tk_comment.enable_standard_buttons()

    def _render_comments(self, domain_commets_objects):
        for domain_comment_obj in domain_commets_objects:
            tk_comment = TkComment(self._comments_inner_frame, domain_obj=domain_comment_obj, controller=self._controller, master_gui=self)
            tk_comment.pack()
            self._tk_comments.append(tk_comment)

        self._comments_scrolled_frame.update_scroll_bars()

    def _render_pagination_bar(self):
        # print(self.comments_count)
        self._paginator = paginator = PaginatorWithCombobox(self._pagination_frame, 5, 10,
                                                            command=self._on_page_change, pagination_style=pagination_style)
        paginator.pack()
        # paginator.pack_forget()

    def _on_page_change(self, *args):
        self._comments_scrolled_frame.set_scroll_y(0.0)
        self.current_page = args[0]
        self._controller.get_comments()

    @staticmethod
    def _clearElementChilderns(element):
        for widget in element.winfo_children():
            widget.destroy()

    def _disable_all_child_elements(self, parent):
        self._travese_children(parent, lambda child: child.config(state=DISABLED))

    def _enable_all_child_elements(self, parent):
        self._travese_children(parent, lambda child: child.config(state=NORMAL))

    def _travese_children(self, parent, visitor):
        for child in parent.winfo_children():
            self._travese_children(child, visitor)
            try:
                visitor(child)
            except:
                pass

    def _hide_paginator(self):
        self._pagination_frame.pack_forget()

    def _show_paginator(self):
        if not self._pagination_frame.winfo_ismapped():
            print("vnatre")
            self._pagination_frame.pack()

    def _show_hide_paginator(self):
        if ceil(self.comments_count / config.COMMENTS_PER_PAGE) < 2:
            self._hide_paginator()
        else:
            self._show_paginator()

    def _on_add_button_click(self):

        def _on_cancel_button_click():
            add_comment_window.destroy()

        def _on_save_button_click():
            # text_content = text.get('1.0', END)
            self._controller.add_comment(text.get(config.TEXT_START_INDEX, config.TEXT_END_INDEX))
            # add_comment_window.grab_release()
            _on_cancel_button_click()
            # self._root.after(5000, lambda : self._controller.add_comment(text_content))


        add_comment_window = Toplevel(self._root)
        add_comment_window.title(config.ADD_WINDOW_TITLE)
        add_comment_window.transient(self._root)
        add_comment_window.grab_set()

        add_comment_window.resizable(False, False)

        outer_warp_frame = Frame(add_comment_window)
        outer_warp_frame.config()
        outer_warp_frame.pack(padx=10, pady=10)

        left_frame = Frame(outer_warp_frame)
        left_frame.pack(side=LEFT)

        right_frame = Frame(outer_warp_frame)
        right_frame.pack(side=RIGHT, padx=(20, 0), anchor=NE)

        text = ScrolledText(left_frame)
        text.pack()
        text.config(width=68, height=12, font='Verdana, 11', spacing1=1, spacing2=2, spacing3=1, wrap='word')
        text.focus_set()

        save_button = Button(right_frame, text='Save', command=_on_save_button_click)
        save_button.grid(row=0, column=0)

        cancel_button = Button(right_frame, text='Cancel', command=_on_cancel_button_click)
        cancel_button.grid(row=1, column=0)

    def update_main_window_layout_min_size(self):
        self._root.update()
        self._root.minsize(self._root.winfo_width(), self._root.winfo_height()+30)
        # print(self._root.winfo_width())
        # print(self._root.winfo_height())
        # pass


