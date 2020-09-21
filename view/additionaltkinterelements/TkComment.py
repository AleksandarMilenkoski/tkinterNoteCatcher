from tkinter import LEFT, RIGHT, NE, Frame, W, X, END, DISABLED, NORMAL
from tkinter.ttk import Button, Style
from view.additionaltkinterelements.ScrolledText import ScrolledText
from stylenameElementOptions import stylename_element_options


class TkComment(Frame):
    def __init__(self, master, domain_obj=None, controller=None, master_gui=None, **kw):
        super().__init__(master, **kw)

        self._master_gui = master_gui
        self._domain_obj = domain_obj
        self._controller = controller
        self._search_phrase = ''

        self._setup_self()
        self._setup_layout()
        self._render_text()
        self._render_buttons()
        self._hide_edit_buttons()
        self.disable_standard_buttons()
        self.enable_standard_buttons()
        # self._show_edit_buttons()
        # self._hide_standard_buttons()
        # self._show_standard_buttons()

    def _setup_self(self):
        self.config(highlightthickness=1, highlightbackground='#a0a0a0')
        self.pack(pady=5, anchor=W, fill=X)

    def _setup_layout(self):
        self._text_container = text_container = Frame(self)
        text_container.pack(side=LEFT, padx=(15, 35), pady=15)

        self._buttons_container = buttons_container = Frame(self)
        buttons_container.pack(side=RIGHT, pady=25, padx=15, anchor=NE)

    def _render_text(self):
        self._text = text = ScrolledText(self._text_container)
        text.pack()
        text.insert('1.0', self._domain_obj.get_comment())
        text.config(width=70, height=15, state='disabled', wrap='word')

    def _render_buttons(self):
        buttons_conainer = self._buttons_container

        self._edit_button = edit_button = Button(buttons_conainer, text='Edit', command=self._on_edit_button_click)
        edit_button.grid(row=0, column=0)

        self._delete_button = delete_button = Button(buttons_conainer, text='Delete')
        delete_button.grid(row=0, column=1)

        self._copy_button = copy_button = Button(buttons_conainer, text='Copy')
        copy_button.grid(row=1, column=0)

        self._save_button = save_button = Button(buttons_conainer, text='Save')
        save_button.grid(row=0, column=2)

        self._cancel_button = cancel_button = Button(buttons_conainer, text='Cancel', command=self._on_cancel_button_click)
        cancel_button.grid(row=1, column=2)

    def _hide_edit_buttons(self):
        self._save_button.grid_remove()
        self._cancel_button.grid_remove()

    def _show_edit_buttons(self):
        self._save_button.grid()
        self._cancel_button.grid()

    def _hide_standard_buttons(self):
        self._edit_button.grid_remove()
        self._delete_button.grid_remove()
        self._copy_button.grid_remove()

    def _show_standard_buttons(self):
        self._edit_button.grid()
        self._delete_button.grid()
        self._copy_button.grid()

    def _on_edit_button_click(self):
        self._hide_standard_buttons()
        self._show_edit_buttons()
        self._text.config(state='normal')
        self._text.focus_set()
        self._master_gui.disable_gui()

    def _on_cancel_button_click(self):
        self._text.delete('1.0', END)
        self._text.insert('1.0', self._domain_obj.get_comment())
        self._text.config(state=DISABLED)
        self._master_gui.enable_gui()
        self._show_standard_buttons()
        self._hide_edit_buttons()

    def disable_standard_buttons(self):
        self._edit_button.config(state='disabled')
        self._delete_button.config(state='disabled')
        self._copy_button.config(state='disabled')

    def enable_standard_buttons(self):
        self._edit_button.config(state='normal')
        self._delete_button.config(state='normal')
        self._copy_button.config(state='normal')

    def mark_text(self, search_phrase):
        self._search_phrase = search_phrase

    def clear_maked_text(self):
        self._search_phrase = ''
