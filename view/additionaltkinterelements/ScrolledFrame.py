from tkinter import Tk, Canvas, N, S, E, W, HORIZONTAL, NW, ALL, Button, CENTER, RIDGE
from view.additionaltkinterelements.AutoHideScrollBar import AutoHideScrollBar
from tkinter.ttk import Frame, Style
from stylenameElementOptions import stylename_element_options

OUTER_FRAME_WRAPPER_BG = '#B1B1B1'


class ScrolledFrame(Frame):

    def __init__(self, parent, **kwargs):
        self._setup_outer_frame_wrapper(parent)
        self._setup_canvas_wrapper()
        self._setup_scroll_bars()
        super().__init__(self.canvas_wrapper, **kwargs)
        self._setup_self()

    def get_outer_frame_wrapper_reference(self):
        return self._outer_wrapper_frame

    def get_canvas_wrapper_reference(self):
        return self.canvas_wrapper

    def update_scroll_bars(self):
        self.update_idletasks()
        self.canvas_wrapper.config(scrollregion=self.canvas_wrapper.bbox(ALL))

    def _setup_outer_frame_wrapper(self, parent):
        self._outer_wrapper_frame = Frame(parent)
        self._outer_wrapper_frame.grid_rowconfigure(0, weight=1)
        self._outer_wrapper_frame.grid_columnconfigure(0, weight=1)
        self._set_outer_frame_style()

    def _setup_canvas_wrapper(self):
        self.canvas_wrapper = Canvas(self._outer_wrapper_frame)
        self.canvas_wrapper.grid(row=0, column=0, sticky=N + S + E + W)
        # canvas.config(bg='red')

    def _setup_self(self):
        x0 = self.winfo_screenwidth()/2
        # print(self.winfo_screenwidth()/2)
        # self.canvas_wrapper.create_window(-100, -100, anchor=NW, window=self)
        # self.config(width=800, borderwidth=12)
        self.canvas_wrapper.create_window(0, 0, anchor=NW, window=self)

        # style = Style()
        # print(self.winfo_class())
        # self.config(style='Inner.TFrame')
        # style.configure('Inner.TFrame', background='olive')
        # stylename_element_options('Inner.TFrame')
        # self.config(bg='green')

    def _setup_scroll_bars(self):
        vertical_scroll_bar = AutoHideScrollBar(self._outer_wrapper_frame)
        vertical_scroll_bar.grid(row=0, column=1, sticky=N + S)
        vertical_scroll_bar.config(command=self.canvas_wrapper.yview)

        horizontal_scroll_bar = AutoHideScrollBar(self._outer_wrapper_frame)
        horizontal_scroll_bar.grid(row=1, column=0, sticky=E + W)
        horizontal_scroll_bar.config(orient=HORIZONTAL, command=self.canvas_wrapper.xview)

        self.canvas_wrapper.config(yscrollcommand=vertical_scroll_bar.set, xscrollcommand=horizontal_scroll_bar.set, highlightthickness=0)

    def _set_outer_frame_style(self):
        outer_style = Style()
        outer_style.configure('Outer.TFrame', background=OUTER_FRAME_WRAPPER_BG)
        self._outer_wrapper_frame.config(style='Outer.TFrame', borderwidth=1, relief=RIDGE)

    def pack(self, **kwargs):
        self._outer_wrapper_frame.pack(**kwargs)

    def grid(self, **kwargs):
        self._outer_wrapper_frame.grid(**kwargs)

    def place(self, **kwargs):
        self._outer_wrapper_frame.place(**kwargs)


if __name__ == '__main__':
    root = Tk()
    root.geometry('400x300')
    scrolled_frame = ScrolledFrame(root)
    scrolled_frame.pack(padx=10, pady=10, anchor=NW, fill='both', expand=True)
    # print(scrolled_frame.get_outer_frame_wrapper_reference().cget('style'))

    for x in range(0, 10):
        Button(scrolled_frame, text='Button ' + str(x)).pack(pady=5, padx=5)

    for i in range(0, 10):
        Button(scrolled_frame, text='Button ' + str(i)).pack(pady=5, padx=5, side='left')

    scrolled_frame.update_scroll_bars()

    root.mainloop()
