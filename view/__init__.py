
from tkinter     import Tk, filedialog
from tkinter.ttk import Frame
# Local imports
from settings import Looks, relative_path
# Widgets
from .menu    import Menu
from .timer   import Timer
from .manage  import Manage
from .lights  import Lights
from .report  import Report

class App(Tk):

    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        # Window settings
        self.title('Productive time')
        self.resizable(False, False)
        self.looks = Looks(self)

        # Widgets and their ranges
        self.header = None 
        self.lights = None 
        self.muteme_visible = False
        self.manage = None # 
        self.manage_visible = False
        self.report = None
        self.report_visible = False
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

        self.header = Menu(self)
        self.timer_widget()

    def prompt_file_name(self) -> str:
        ''' Prompts the user for a file name '''
        cur_dur = relative_path('')
        return filedialog.asksaveasfilename(initialdir=cur_dur,title = "Select file",filetypes = (("csv files","*.csv"),("all files","*.*")))

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
            self.controller.muteme_color = 'noColor'
            self._reorder_timers()
        
        if len(self.timers) == 0:
            self.timer_widget()

    def _reorder_timers(self):
        ''' Reorders the timers when one is removed '''
        row_buffer = 1
        for i, timer in enumerate(self.timers):
            timer.grid_widgets(row=i+row_buffer)

    def manage_widget(self):
        ''' Opens the productivity window '''
        if not self.manage_visible:
            if self.muteme_visible:
                self.lights.destroy()
                self.muteme_visible = False
            if self.report_visible:
                self.report.destroy()
                self.report_visible = False
            self.manage_visible = True           
            self.manage = Manage(self)
        else:
            self.manage_visible = False
            self.manage.destroy()

    def lights_widget(self):
        ''' Opens the lights window '''
        if not self.muteme_visible:
            if self.manage_visible:
                self.manage.destroy()
                self.manage_visible = False
            if self.report_visible:
                self.report.destroy()
                self.report_visible = False
            self.muteme_visible = True
            self.lights = Lights(self)
        else:
            self.muteme_visible = False
            self.lights.destroy()

    def report_widget(self):
        ''' Opens the report window '''
        if not self.report_visible:
            if self.muteme_visible:
                self.lights.destroy()
                self.muteme_visible = False
            if self.manage_visible:
                self.manage.destroy()
                self.manage_visible = False
            self.report_visible = True
            self.report = Report(self)
            weekly_report = self.controller.get_timer_report('7')
            self.report.update_report(weekly_report)
        else:
            self.report_visible = False
            self.report.destroy()
