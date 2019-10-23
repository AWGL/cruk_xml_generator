import tkinter as tk
import logging


class MessageBox(tk.Tk):

    def __init__(self, box):
        tk.Tk.__init__(self, box)
        self.box = box
        #self.geometry("800x500")
        self.grid()
        self.eval('tk::PlaceWindow %s center' % self.winfo_pathname(self.winfo_id())) # Places popup in middle of screen
        self.mybutton = tk.Button(self, text="OK")
        self.mybutton.grid(column=0, row=1, sticky='EW')
        self.mybutton.bind("<ButtonRelease-1>", self.button_callback)
        self.popup_text = tk.Text(self, state="disabled")
        self.popup_text.grid(column=0, row=0)

    def button_callback(self, event):
        self.destroy()


class MyHandlerText(logging.StreamHandler):
    def __init__(self, textctrl):
        logging.StreamHandler.__init__(self) # initialize parent
        self.textctrl = textctrl

    def emit(self, record):
        msg = self.format(record)
        self.textctrl.config(state="normal")
        self.textctrl.insert("end", msg + "\n")
        self.flush()
        self.textctrl.config(state="disabled")
