import tkinter as tk
from tkinter import ttk
import logging
import datetime


class MessageBox(tk.Tk):
    '''
    def __init__(self,parent):
        tk.Tk.__init__(self,parent)
        self.parent = parent

        self.grid()

        self.mybutton = tk.Button(self, text="ClickMe")
        self.mybutton.grid(column=0,row=0,sticky='EW')
        self.mybutton.bind("<ButtonRelease-1>", self.button_callback)

        self.popup_text = tk.Text(self, state="disabled")
        self.popup_text.grid(column=0, row=1)

    def button_callback(self, event):
        now = datetime.datetime.now()
        module_logger = logging.getLogger("report_CRUK")
        module_logger.info(now)


    '''
    def __init__(self, box):
        tk.Tk.__init__(self, box)
        self.box = box

        self.grid()

        #self.button = ttk.Button(box, text="OK") #, command=box.destroy)
        #self.button.pack()
        self.eval('tk::PlaceWindow %s center' % self.winfo_pathname(self.winfo_id())) # Places popup in middle of screen
        self.mybutton = tk.Button(self, text="ClickMe")
        self.mybutton.grid(column=0, row=0, sticky='EW')
        self.mybutton.bind("<ButtonRelease-1>", self.button_callback)
        self.popup_text = tk.Text(self, state="disabled")
        self.popup_text.grid(column=0, row=1)


        #label = ttk.Label(popup, text="XML and PDF generated successfully", font=("Verdana", 10))
        #lable = ttk.Label(popup, text=popup_text, font=("Verdana", 10))  # TODO tmp
        #lable.pack(side="left", fill=None, pady=10)  # TODO tmp
        #label.pack(side="top", fill="x", pady=10)


    def button_callback(self, event):
        now = datetime.datetime.now()
        module_logger = logging.getLogger("report_CRUK")
        module_logger.info(now)
