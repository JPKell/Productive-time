from tkinter import Tk
from tkinter.ttk import Frame

from widgets import Header, Lights, Timer, Productivity
from looks import Looks

class App(Tk):

    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        # Window settings
        self.title('Productivity timing')
        self.resizable(False, False)
        self.looks = Looks(self)

        # Widgets and their ranges
        self.header = None 
        self.lights = None 
        self.lights_visible = False
        self.productivity = None # 
        self.productivity_visible = False
        self.timers = [] 

        # Ui settings
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)
        self.columnconfigure(3, weight=1)
        self.columnconfigure(4, weight=1)
        self.columnconfigure(5, weight=1)
        self.columnconfigure(6, weight=1)
        self.columnconfigure(7, weight=1)
        self.columnconfigure(8, weight=1)
        self.columnconfigure(9, weight=1)

        self._build_ui()


    def _build_ui(self):
        self.frame = Frame(self)
        self.frame.columnconfigure(0, weight=1)
        self.frame.grid(row=0, column=0, sticky='nsew')

        self.header = Header(self)
        self.timer_widget()


    def timer_widget(self):
        ''' Builds a new timer widget. Timers start at row 50 to leave room above for things to push them down'''
        row_buffer = 1
        timer_row = len(self.timers)+row_buffer
        self.timers.append(Timer(self,row=timer_row))

    def remove_timer(self, timer:Frame):
        ''' Checks if any timers are done '''
        if timer in self.timers:
            self.timers.remove(timer)
            timer.delete_timer()
            self._reorder_timers()
        
        if len(self.timers) == 0:
            self.timer_widget()

    def _reorder_timers(self):
        ''' Reorders the timers when one is removed '''
        row_buffer = 1
        for i, timer in enumerate(self.timers):
            timer.grid_widgets(row=i+row_buffer)

    def productivity_widget(self):
        ''' Opens the productivity window '''
        if not self.productivity_visible:
            if self.lights_visible:
                self.lights.destroy()
                self.lights_visible = False
            self.productivity_visible = True           
            self.productivity = Productivity(self)
        else:
            self.productivity_visible = False
            self.productivity.destroy()

    def lights_widget(self):
        ''' Opens the lights window '''
        if not self.lights_visible:
            if self.productivity_visible:
                self.productivity.destroy()
                self.productivity_visible = False
            self.lights_visible = True
            self.lights = Lights(self)
        else:
            self.lights_visible = False
            self.lights.destroy()


if __name__ == '__main__':
    app = App()
    app.mainloop()