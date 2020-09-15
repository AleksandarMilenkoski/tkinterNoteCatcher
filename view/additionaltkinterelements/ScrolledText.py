from tkinter import Tk, N, S, E, W, HORIZONTAL, Text, WORD
from view.additionaltkinterelements.AutoHideScrollBar import AutoHideScrollBar
from tkinter.ttk import Frame


class ScrolledText(Text):

    def __init__(self, parent, **kwargs):
        self._setup_outer_frame_wrapper(parent)
        super().__init__(self._outer_wrapper_frame, **kwargs)
        self._setup_scroll_bars()
        self._setup_self()

    def get_outer_frame_wrapper_reference(self):
        return self._outer_wrapper_frame

    def _setup_outer_frame_wrapper(self, parent):
        self._outer_wrapper_frame = Frame(parent)
        self._outer_wrapper_frame.grid_rowconfigure(0, weight=1)
        self._outer_wrapper_frame.grid_columnconfigure(0, weight=1)

    def _setup_scroll_bars(self):
        vertical_scroll_bar = AutoHideScrollBar(self._outer_wrapper_frame)
        vertical_scroll_bar.grid(row=0, column=1, sticky=N + S)
        vertical_scroll_bar.config(command=self.yview)

        horizontal_scroll_bar = AutoHideScrollBar(self._outer_wrapper_frame)
        horizontal_scroll_bar.grid(row=1, column=0, sticky=E + W)
        horizontal_scroll_bar.config(orient=HORIZONTAL, command=self.xview)

        self.config(yscrollcommand=vertical_scroll_bar.set, xscrollcommand=horizontal_scroll_bar.set)

    def _setup_self(self):
        super().grid(row=0, column=0, sticky=N + S + E + W)
        self.config(wrap=WORD)

    def pack(self, **kwargs):
        self._outer_wrapper_frame.pack(**kwargs)

    def grid(self, **kwargs):
        self._outer_wrapper_frame.grid(**kwargs)

    def place(self, **kwargs):
        self._outer_wrapper_frame.place(**kwargs)


if __name__ == '__main__':
    root = Tk()
    root.geometry('400x300')
    scrolled_text = ScrolledText(root)
    scrolled_text.pack(pady=20, anchor=W, padx=10)
    scrolled_text.config(width=50, height=10)

    root.mainloop()
