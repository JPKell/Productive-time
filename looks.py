from tkinter import font
from tkinter.ttk import Style

class Looks(Style):
    def __init__(self, master) -> None:
        super().__init__(master)
        self.theme_use('clam')
        self.configure('TButton', font=('Arial', 10))
        self.configure('TLabel', font=('Arial', 24))