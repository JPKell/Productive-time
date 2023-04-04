from tkinter.ttk import Style

class Looks(Style):
    ''' Sets up the look of the app.
    
        The theme is based on the forest-dark theme from https://github.com/rdbende/Forest-ttk-theme
        
    '''
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

    def __init__(self, master) -> None:
        super().__init__(master)
        master.tk.call('source', '/home/jpk/gits/eMetuM/theme/forest-dark.tcl')
        self.theme_use('forest-dark')

        self.configure('red.TButton',    foreground=self.red)
        self.configure('yellow.TButton', foreground=self.yellow)
        self.configure('green.TButton',  foreground=self.green)
        self.configure('cyan.TButton',   foreground=self.cyan)
        self.configure('blue.TButton',   foreground=self.blue)
        self.configure('purple.TButton', foreground=self.purple)
        self.configure('white.TButton',  foreground=self.white)
        self.configure('black.TButton',  foreground=self.black)

        self.configure('Timer.TLabel',        foreground=self.white)
        self.configure('red.TLabel',    foreground=self.red)
        self.configure('yellow.TLabel', foreground=self.yellow)
        self.configure('green.TLabel',  foreground=self.green)
        self.configure('cyan.TLabel',   foreground=self.cyan)
        self.configure('blue.TLabel',   foreground=self.blue)
        self.configure('purple.TLabel', foreground=self.purple)
        self.configure('white.TLabel',  foreground=self.white)
        
