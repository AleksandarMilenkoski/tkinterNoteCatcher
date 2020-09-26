from tkinter import Tk, Canvas, N, S, E, W, HORIZONTAL, NW, ALL, Button, CENTER, RIDGE, Label
from view.additionaltkinterelements.AutoHideScrollBar import AutoHideScrollBar
from tkinter.ttk import Frame, Style
from stylenameElementOptions import stylename_element_options

OUTER_FRAME_WRAPPER_BG = '#B1B1B1'

ALIGN_LEFT = 'left'
ALIGN_RIGHT = 'righ'
ALIGN_CENTER = 'center'
SCROLL_RATE = 0.05

class ScrolledFrame(Frame):

    def __init__(self, parent, content_orientation=ALIGN_LEFT, **kwargs):
        self._content_alignment = content_orientation
        self._setup_outer_frame_wrapper(parent)
        self._set_outer_frame_style()
        self._setup_canvas_wrapper()
        self._setup_scroll_bars()
        self._setup_inner_canvas_warpper_frame()
        super().__init__(self._inner_canvas_warpper_frame, **kwargs)
        self._setup_self()
        # self._setup_self_style()

    def get_outer_frame_wrapper_reference(self):
        return self._outer_wrapper_frame

    def get_canvas_wrapper_reference(self):
        return self._canvas_wrapper

    def update_scroll_bars(self):
        self.update_idletasks()
        # self.update()
        # print(self.winfo_width())
        self._canvas_wrapper.config(scrollregion=self._canvas_wrapper.bbox(ALL))
        # self._canvas_wrapper.bind('<Configure>', lambda event: self._on_canvas_resize())

    def _setup_outer_frame_wrapper(self, parent):
        self._outer_wrapper_frame = Frame(parent)
        self._outer_wrapper_frame.grid_rowconfigure(0, weight=1)
        self._outer_wrapper_frame.grid_columnconfigure(0, weight=1)

    def _setup_canvas_wrapper(self):
        self._canvas_wrapper = canvas_wrapper = Canvas(self._outer_wrapper_frame)
        canvas_wrapper.grid(row=0, column=0, sticky=N + S + E + W)
        # canvas_wrapper.bind_all('<Button-4>', self._on_mouse_wheel_scroll_up)
        # canvas_wrapper.bind_all('<Button-5>', self._on_mouse_wheel_scroll_down)

        if self._content_alignment != ALIGN_LEFT:
            canvas_wrapper.bind('<Configure>', lambda event: self._on_canvas_resize())

        # canvas_wrapper.config(bg='white')

    def _setup_self(self):
        super().pack()

    def _setup_scroll_bars(self):
        vertical_scroll_bar = AutoHideScrollBar(self._outer_wrapper_frame)
        vertical_scroll_bar.grid(row=0, column=1, sticky=N + S)
        vertical_scroll_bar.config(command=self._canvas_wrapper.yview)

        horizontal_scroll_bar = AutoHideScrollBar(self._outer_wrapper_frame)
        horizontal_scroll_bar.grid(row=1, column=0, sticky=E + W)
        horizontal_scroll_bar.config(orient=HORIZONTAL, command=self._canvas_wrapper.xview)

        self._canvas_wrapper.config(yscrollcommand=vertical_scroll_bar.set, xscrollcommand=horizontal_scroll_bar.set, highlightthickness=0)

    def _set_outer_frame_style(self):
        self._outer_wrapper_frame.config(style='Outer.TFrame', borderwidth=1, relief=RIDGE)
        Style().configure('Outer.TFrame', background=OUTER_FRAME_WRAPPER_BG)

    def _on_canvas_resize(self):

        offset = 0
        canvas_width = self._canvas_wrapper.winfo_width()
        inner_frame_width = self.winfo_width()

        if canvas_width > inner_frame_width and self._content_alignment == ALIGN_CENTER:
            offset = (canvas_width - inner_frame_width) // 2
        else:
            offset = canvas_width - inner_frame_width

        if offset < 0:
            offset = 0

        self.pack_configure(padx=(offset, 0))

        # print('canvas_width ' + str(canvas_width))
        # print('inner_canvas_warpper_frame_width ' + str(self._inner_canvas_warpper_frame.winfo_width()))
        # print('inner_frame_width ' + str(inner_frame_width))
        # print('offset ' + str(offset))

        return 'break'

    def pack(self, **kwargs):
        self._outer_wrapper_frame.pack(**kwargs)

    def grid(self, **kwargs):
        self._outer_wrapper_frame.grid(**kwargs)

    def place(self, **kwargs):
        self._outer_wrapper_frame.place(**kwargs)

    def _setup_self_style(self):
        self.config(style='InnerFrame.TFrame')
        # Style().configure('InnerFrame.TFrame', background='red')

    def _setup_inner_canvas_warpper_frame(self):
        self._inner_canvas_warpper_frame = inner_canvas_warpper_frame = Frame(self._canvas_wrapper,
                                                                              style='InnerCanvasWrapper.TFrame')
        self._canvas_wrapper.create_window(0, 0, anchor=NW, window=inner_canvas_warpper_frame, tag='inner_frame')
        # Style().configure('InnerCanvasWrapper.TFrame', background='orange')

        # print(inner_canvas_warpper_frame)
        #
        # self.label = label = Label(inner_canvas_warpper_frame, text='Pece')
        # label.pack(ipadx=10)
        # print(label)
        #
        # frame_one = Frame(inner_canvas_warpper_frame)
        # frame_one.pack()
        #
        # label_two = Label(frame_one, text='Label Two')
        # label_two.pack()
        # print(label_two)

    def set_scroll_y(self, val):
        self._canvas_wrapper.yview_moveto(val)
        # print(self._canvas_wrapper.yview())

    def _on_mouse_wheel_scroll_up(self, event):
        self._canvas_wrapper.yview_moveto(self._canvas_wrapper.yview()[0] - SCROLL_RATE)

    def _on_mouse_wheel_scroll_down(self, event):
        self._canvas_wrapper.yview_moveto(self._canvas_wrapper.yview()[0] + SCROLL_RATE)
        print(dir(event))
        print(event.keycode)
        # print(event.height)
        # print('wheel')
        # self._canvas_wrapper.yview_scroll(-1*(event.delta/120), "units")




if __name__ == '__main__':
    root = Tk()
    root.geometry('400x300')
    scrolled_frame = ScrolledFrame(root)
    scrolled_frame.pack(padx=10, pady=10, anchor=NW, fill='both', expand=True)
    # print(scrolled_frame)
    # print(scrolled_frame.get_outer_frame_wrapper_reference().cget('style'))

    for x in range(0, 10):
        Button(scrolled_frame, text='Button ' + str(x)).pack(pady=5, padx=5)

    for i in range(0, 10):
        Button(scrolled_frame, text='Button ' + str(i)).pack(pady=5, padx=5, side='left')

    scrolled_frame.update_scroll_bars()

    root.mainloop()
