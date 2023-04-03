from tkinter import font
from tkinter.ttk import Style

# Widgets used
# View   : Frame
# Header : Buttons
# Timer  : Button, Label, OptionMenu
# Produc : Button, Label, OptionMenu, Combobox, Spinbox, LabelFrame, Checkbutton, Frame
# Lights : Frame, Button, Labelframe

bg     = "#424242"
btn    = "#323232"
white  = "#ffffff"
red    = "#ff0000"
yellow = "#ffff00"
green  = "#00ff00"
cyan   = "#00ffff"
blue   = "#0000ff"
purple = "#ff00ff"
white  = "#ffffff"
black  = "#000000"

class Looks(Style):
    def __init__(self, master) -> None:
        super().__init__(master)
        master.tk.call('source', 'forest-dark.tcl')
        self.theme_use('forest-dark')

        self.configure('Red.TButton',    foreground=red)
        self.configure('Yellow.TButton', foreground=yellow)
        self.configure('Green.TButton',  foreground=green)
        self.configure('Cyan.TButton',   foreground=cyan)
        self.configure('Blue.TButton',   foreground=blue)
        self.configure('Purple.TButton', foreground=purple)
        self.configure('White.TButton',  foreground=white)
        self.configure('Black.TButton',  foreground=black)

        self.configure('Timer.TLabel', foreground=white)
        self.configure('Timer.red.TLabel', foreground=red)
        self.configure('Timer.yellow.TLabel', foreground=yellow)
        self.configure('Timer.green.TLabel', foreground=green)
        self.configure('Timer.cyan.TLabel', foreground=cyan)
        self.configure('Timer.blue.TLabel', foreground=blue)
        self.configure('Timer.purple.TLabel', foreground=purple)
        self.configure('Timer.white.TLabel', foreground=white)
        
