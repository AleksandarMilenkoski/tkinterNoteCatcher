# from tkinter import
from tkinter.ttk import Frame, Button

class Comment(Frame):
    def __init__(self, master, domain_obj, **kw):
        self._domain_obj = domain_obj
        super().__init__(master, **kw)