import config
from tkinter import Tk, PhotoImage, Frame, BOTH, GROOVE, TRUE, X, Y, Menu, LEFT, StringVar, N, W, NW, TOP, RIGHT, \
    NE, FLAT, DISABLED, NORMAL
from tkinter.ttk import Label, Entry, Button
from view.additionaltkinterelements.ScrolledFrame import ScrolledFrame
from view.additionaltkinterelements.TkComment import TkComment
from view.helpers.paginator.PaginatorWithCombobox import PaginatorWithCombobox, pagination_style
from math import ceil

class CommentsView:
    '''
    CommentsView class
    '''

    def __init__(self, controller):
        self._controller = controller
        self._tk_comments = []
        self.current_page = 1
        self.comments_count = 0
        self.serarch_phrase = ''
        self.main()

    def main(self):
        # root window
        self.root = Tk()

        # print(self.root.cget('bg'))
        # window setup
        self._set_main_window_title()
        self._set_main_window_dimensions()
        # self._position_main_window()
        self._set_main_window_fav_icon()
        self._set_main_menu()
        self._set_main_window_layout()
        self._render_search_bar()
        # self._render_comments()
        # self._update_comments()
        self._render_pagination_bar()

        # main loop window
        # self.root.mainloop()

    def main_loop(self):
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
        self._main_menu = main_menu = Menu(self.root)

        main_menu.add_command(label = 'Add Comment')

        self.root.config(menu = main_menu)

    def _set_main_window_layout(self):
        main_frame = Frame(self.root)
        # main_frame.config(bg = 'white')
        main_frame.pack(fill='both', expand=True, pady=(0, 20))

        self._search_frame = search_frame = Frame(main_frame)
        search_frame.pack()
        # search_frame.config(bg='red')

        comments_outer_frame = Frame(main_frame, borderwidth=5)
        comments_outer_frame.pack(side=TOP, anchor=N, ipadx=10, ipady=10, padx=10, pady=(10, 20), fill=BOTH, expand=True)
        self._comments_scrolled_frame = comments_scrolled_frame = ScrolledFrame(comments_outer_frame)
        comments_scrolled_frame.pack(fill=BOTH, expand=True)
        self._comments_inner_frame = comments_inner_frame = Frame(comments_scrolled_frame)
        comments_inner_frame.pack(ipadx=10, pady=10)

        self._pagination_frame = pagination_frame = Frame(main_frame)
        # pagination_frame.pack(side=TOP, anchor=N, ipadx=10, ipady=10, padx=10, pady=10)
        pagination_frame.pack()

    def _render_search_bar(self):
        self._serach_value = serach_value = StringVar()

        search_container = Frame(self._search_frame)
        search_container.pack(side=TOP, anchor=N, padx=10, pady=(20,10))

        Label(search_container, text=config.SEARCH_LABEL_TEXT).pack(side=LEFT)

        Entry(search_container, textvariable=serach_value, width=30).pack(side=LEFT, padx=(5, 10))

        Button(search_container, text='Search').pack(side=LEFT)

        Button(search_container, text='Clear').pack(side=LEFT)

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
           self._tk_comments.append(TkComment(self._comments_inner_frame, domain_obj=domain_comment_obj,
                                              controller=self._controller, master_gui=self))

        self._comments_scrolled_frame.update_scroll_bars()

    def _render_pagination_bar(self):
        # print(self.comments_count)
        self._paginator = paginator = PaginatorWithCombobox(self._pagination_frame, 5, 10,
                                                            command=self._on_page_change, pagination_style=pagination_style)
        paginator.pack()
        # paginator.pack_forget()

    def _on_page_change(self, *args):
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





