from tkinter import LEFT, RIGHT, NE, Frame, W, X, END, DISABLED, NORMAL
from tkinter.ttk import Button, Style
from view.additionaltkinterelements.ScrolledText import ScrolledText
from tkinter.messagebox import askokcancel
from stylenameElementOptions import stylename_element_options
import pyperclip
import html
import config


class TkComment(Frame):
    def __init__(self, master, domain_obj=None, controller=None, master_gui=None, **kw):
        super().__init__(master, **kw)

        self._master_gui = master_gui
        self._domain_obj = domain_obj
        self._controller = controller
        self._search_phrase = ''

        # self._setup_self()
        self._setup_layout()
        self._render_text()
        self._render_buttons()
        self._hide_edit_buttons()
        self._setup_style()
        # self.disable_standard_buttons()
        # self.enable_standard_buttons()
        # self._show_edit_buttons()
        # self._hide_standard_buttons()
        # self._show_standard_buttons()

    def _setup_self(self):
        self.pack()

    def _setup_layout(self):
        self._text_container = text_container = Frame(self)
        text_container.pack()

        self._buttons_container = buttons_container = Frame(self)
        buttons_container.pack()

    def _render_text(self):
        self._text = text = ScrolledText(self._text_container)
        text.pack()
        text.insert(config.TEXT_START_INDEX, html.unescape(self._domain_obj.get_comment()))
        text.config(state='disabled')

    def _render_buttons(self):
        buttons_conainer = self._buttons_container

        self._edit_button = edit_button = Button(buttons_conainer, text='Edit', command=self._on_edit_button_click)
        edit_button.grid(row=0, column=0)

        self._delete_button = delete_button = Button(buttons_conainer, text='Delete', command=self._on_delete_button_click)
        delete_button.grid(row=0, column=1)

        self._copy_button = copy_button = Button(buttons_conainer, text='Copy', command=self._on_copy_button_click)
        copy_button.grid(row=1, column=0)

        self._save_button = save_button = Button(buttons_conainer, text='Save', command=self._on_save_button_click)
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
        self._clear_text_makup()
        self._text.focus_set()
        self._master_gui.disable_gui()

    def _on_cancel_button_click(self):
        self._text.delete(config.TEXT_START_INDEX, END)
        self._text.insert(config.TEXT_START_INDEX, self._domain_obj.get_comment())
        self._text.config(state=DISABLED)
        self._master_gui.enable_gui()
        self._show_standard_buttons()
        self._hide_edit_buttons()
        if self._search_phrase != '':
            self.mark_text(self._search_phrase)

    def _on_delete_button_click(self):
        if askokcancel('Delete Comment', 'Are you sure?'):
            self._controller.delete_comment(self._domain_obj)
        # print('delete')

    def _on_copy_button_click(self):
        pyperclip.copy(self._domain_obj.get_comment())

    def _on_save_button_click(self):
        content_text = self._text.get(config.TEXT_START_INDEX, config.TEXT_END_INDEX)
        # print(content_text)
        if content_text != self._domain_obj.get_comment():
            self._domain_obj.set_comment(content_text)
            self._controller.edit_comment(self._domain_obj)
            self._master_gui.enable_gui()
        else:
            self._on_cancel_button_click()

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
        content_text = self._text
        # print(search_phrase)
        start_pos = config.TEXT_START_INDEX
        while True:
            start_pos = content_text.search(search_phrase, start_pos, nocase=True, stopindex=END)
            if not start_pos:
                break
            end_pos = '{}+{}c'.format(start_pos, len(search_phrase))
            content_text.tag_add('match', start_pos, end_pos)
            start_pos = end_pos
        # content_text.tag_config('match', foreground='red', background='yellow')
        content_text.tag_config('match', background='yellow')

    def clear_maked_text(self):
        self._search_phrase = ''

    def _clear_text_makup(self):
        self._text.delete(config.TEXT_START_INDEX, END)
        self._text.insert(config.TEXT_START_INDEX, html.unescape(self._domain_obj.get_comment()))

    def _setup_style(self):
        self.pack_configure(pady=5, anchor=W, fill=X)
        self.config(highlightthickness=1, highlightbackground='#a0a0a0')

        self._text_container.pack_configure(side=LEFT, padx=(15, 35), pady=15)

        self._buttons_container.pack_configure(side=RIGHT, pady=25, padx=15, anchor=NE)

        self._text.config(width=68, height=12, font='Verdana, 11', spacing1=1, spacing2=2, spacing3=1, wrap='word')
