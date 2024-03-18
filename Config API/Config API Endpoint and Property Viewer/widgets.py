# 
# 
# 
# 
'''
Widget Classes
'''

from tkinter import *
from tkinter import ttk, messagebox


class searchbar(ttk.Frame):
    def __init__(self, master=None, column=0, row=0, command = None):
        super().__init__(master)
        self.master = master
        self.grid(column=column, row=row, sticky=NSEW)
        self.searchInput = StringVar()
        self.input = Entry(self, textvariable= self.searchInput)
        self.input.grid(column=1, row=0, sticky=NSEW)
        self.button = Button(self, text='Search', command=command)
        self.button.grid(column=2, row=0, sticky=NSEW)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=0)
        self.rowconfigure(0, weight=1)
        self.input.event_add('<<EnterPress>>', '<Return>')
        self.input.bind('<<EnterPress>>', command)

class vscroll(ttk.Scrollbar):
    def __init__(self, master=None, widget=None):
        super().__init__(master, orient=VERTICAL, command=widget.yview)
        self.master = master
        info = widget.grid_info()
        self.grid(column=info['column'] + 1, row=0, sticky=NSEW)

class hscroll(ttk.Scrollbar):
    def __init__(self, master=None, widget=None):
        super().__init__(master, orient=HORIZONTAL, command=widget.xview)
        self.master = master
        info = widget.grid_info()
        self.grid(column=0, row=info['row'] + 1, sticky=NSEW)

class treevscroll(ttk.Frame):
    def __init__(self, master=None, column=0, row=0, columns=None):
        super().__init__(master)
        self.master = master
        self.grid(column=column, row=row, sticky=NSEW)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.treev = ttk.Treeview(self, show='tree', columns = tuple(columns), displaycolumns=())
        self.treev.column("#0", minwidth = 1000)
        self.treev.grid(column=0, row=0, sticky=NSEW)
        self.scrollbar = vscroll(self, self.treev)
        self.hscrollbar = hscroll(self,self.treev)
        self.treev.configure(yscrollcommand=self.scrollbar.set, xscrollcommand=self.hscrollbar.set)


class textscroll(ttk.Frame):
    def __init__(self, master=None, column=0, row=0):
        super().__init__(master)
        self.master = master
        self.grid(column=column, row=row, sticky=NSEW)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.text = Text(self)
        self.text.grid(column=0, row=0, sticky=NSEW)
        self.scrollbar = vscroll(self,self.text)
        self.text.configure(yscrollcommand=self.scrollbar.set)
        
        

    # Update the whole text box
    def update(self, strings: list):
        self.text.config(state=NORMAL)
        self.text.delete(0.0, END)
        [self.text.insert(END, string, tags) for string, tags in strings]
        self.text.config(state=DISABLED)
    
    # Append data to the end of the existing content
    def append(self, string, tags= None):
        self.text.config(state=NORMAL)
        self.text.insert(END, string, tags)
        self.text.config(state=DISABLED)

    # Clear contents of text box
    def clear(self):
        self.text.config(state=NORMAL)
        self.text.delete(0.0, END)
        self.text.config(state=DISABLED)