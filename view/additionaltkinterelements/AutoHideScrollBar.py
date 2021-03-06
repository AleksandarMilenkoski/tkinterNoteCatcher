from tkinter import TclError
from tkinter.ttk import Scrollbar

class AutoHideScrollBar(Scrollbar):

    # Defining set method with all
    # its parameter
    def set(self, low, high):
        flag = False
        if float(low) <= 0.0 and float(high) >= 1.0:

            # Using grid_remove
            self.tk.call("grid", "remove", self)
        else:
            self.grid()
            flag=True
        Scrollbar.set(self, low, high)

        return flag

    # Defining pack method
    def pack(self, **kw):

        # If pack is used it throws an error
        raise (TclError, "pack cannot be used with \
               this widget")

        # Defining place method

    def place(self, **kw):

        # If place is used it throws an error
        raise (TclError, "place cannot be used with \
               this widget")

        # creating tkinter window