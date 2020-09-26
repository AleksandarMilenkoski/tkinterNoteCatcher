from tkinter import IntVar, Frame, DISABLED, NORMAL
from tkinter.ttk import Combobox, Style
from view.helpers.paginator.Paginator import Paginator


class PaginatorWithCombobox(Paginator):

    def __init__(self, master, displayed_pages, total_pages, background=None, current_page=None, start_page=1,
                 prev_button="Prev", next_button="Next", first_button="First", last_button="Last",
                 hide_controls_at_edge=False, command=None, pagination_style=None):

        self._create_outer_wrapper_layout_frame(master)

        self._create_checkbox_style_config(pagination_style)

        super().__init__(self._outer_paginator_frame, displayed_pages, total_pages, background, current_page,
                         start_page, prev_button, next_button, first_button, last_button, hide_controls_at_edge,
                         command, pagination_style)

    def _render_pagination(self, current_page, prev_button, next_button, first_button, last_button, displayed_pages,
                           start_page, end_page, spacing, hide_controls_at_edge):

        super()._render_pagination(current_page, prev_button, next_button, first_button, last_button, displayed_pages,
                                   start_page, end_page, spacing, hide_controls_at_edge)
        self._render_combobox()

    def _on_click_page(self, new_page):
        super()._on_click_page(new_page)
        self._update_combobox()

    def _update_labels(self):
        super()._update_labels()
        self._update_combobox()

    def update(self, total_pages, current_page):
        self._combobox.config(values=[page for page in range(1, total_pages + 1)],
                              width=self._count_number_positions(self._total_pages))

        self._total_pages = total_pages
        self._current_page = current_page

        self._update_first_last_page()

        self._update_labels()


    def _render_combobox(self):
        self._combobox = combobox = Combobox(self._outer_combobox_frame)
        self._combobox_value = combobox_value = IntVar()
        combobox.pack(padx=(self._label_spacing + 4, 0))
        # print(self._label_spacing)
        combobox.config(values=[page for page in range(1, self.total_pages+1)], textvariable=combobox_value,
                        **self._combobox_style['config'], width=self._count_number_positions(self._total_pages))
        combobox.config(style='Pagination.TCombobox')
        style = Style()
        style.configure('Pagination.TCombobox', **self._combobox_style['style'])
        combobox_value.set(self._current_page)

        combobox.bind('<<ComboboxSelected>>', lambda e: self._on_combobox_change())

    def _on_combobox_change(self):
        self._current_page = current_page = self._combobox_value.get()
        self._command(current_page)
        self._update_first_last_page()
        self._update_labels()

    def _create_outer_wrapper_layout_frame(self, parent):
        outer_layout_frame = Frame(parent)
        outer_layout_frame.pack()
        self._outer_paginator_frame = outer_paginator_frame = Frame(outer_layout_frame)
        outer_paginator_frame.grid(row=0, column=0)
        self._outer_combobox_frame = outer_combobox_frame = Frame(outer_layout_frame)
        outer_combobox_frame.grid(row=0, column=1)

    def _create_checkbox_style_config(self, pagination_style):
        self._combobox_style = checkbox_style = {}
        if 'combobox_padding' in pagination_style or 'combobox_borderwidth' in pagination_style:
            checkbox_style['style'] = {}

            if 'combobox_padding' in pagination_style:
                checkbox_style['style']['padding'] = pagination_style['combobox_padding']

            if 'combobox_borderwidth' in pagination_style:
                checkbox_style['style']['borderwidth'] = pagination_style['combobox_borderwidth']

        if 'combobox_font' in pagination_style:
            checkbox_style['config'] = {}
            checkbox_style['config']['font'] = pagination_style['combobox_font']

        # print(checkbox_style)

    def _update_combobox(self):
        self._combobox_value.set(self._current_page)

    def _update_first_last_page(self):
        current_page = self._current_page

        tmp_start_page = current_page - (self._displayed_pages // 2)
        tmp_end_page = current_page + (self._displayed_pages // 2)

        if self._displayed_pages % 2 == 0:
            tmp_start_page += 1

        if tmp_start_page < 1:
            tmp_start_page = 1
            tmp_end_page = self._displayed_pages

        if tmp_end_page > self._total_pages:
            tmp_end_page = self._total_pages
            tmp_start_page = tmp_end_page - self._displayed_pages + 1

        if tmp_start_page < 1:
            tmp_start_page = 1

        # print(tmp_start_page)
        # print(tmp_end_page)

        self._start_page = tmp_start_page
        self._end_page = tmp_end_page

    @staticmethod
    def _count_number_positions(number):
        positions = 0
        while number % 10 or number // 10:
            positions += 1
            number //= 10

        return positions

    def disable(self):
        super().disable()
        self._combobox.config(state=DISABLED)

    def enable(self):
        super().enable()
        self._combobox.config(state=NORMAL)


pagination_style = {
    "button_spacing": 3,
    "button_padx": 12,
    "button_pady": 6,
    "normal_button": {
        "font": ("Verdana", 10),
        "foreground": "#717171",
        "activeforeground": "#717171",
        "background": "#e9e9e9",
        "activebackground": "#fefefe"
    },
    "selected_button": {
        "font": ("Verdana", 10, "bold"),
        "foreground": "#f0f0f0",
        "activeforeground": "#f0f0f0",
        "background": "#616161",
        "activebackground": "#616161"
    },
    'combobox_padding': (4, 4),
    'combobox_font': ('Verdana', 10),
    'combobox_borderwidth': 3
}

if __name__ == "__main__":
    import tkinter as tk
    from tkinter import Tk, X, W

    root = Tk()

    page = tk.Frame()
    page.pack()

    def print_page(page_number):
        print("page number %s" % page_number)

    row = tk.Frame(page)
    row.pack(padx=10, pady=4, fill=X)

    tk.Label(row, text="Pagination").pack(anchor=W)

    pagination = PaginatorWithCombobox(row, 5, 50, command=print_page, pagination_style=pagination_style)
    # pagination = Paginator(row, 5, 50, command=print_page, pagination_style=pagination_style3)
    pagination.pack(pady=10, anchor=W)
    # print(pagination.__dir__())
    # print(pagination.current_page)
    pagination.update(70, 1, 1)
    # pagination.select_page(20)

    root.mainloop()
