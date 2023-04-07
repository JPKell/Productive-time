import csv

from modules.db     import Db
from modules.device import MuteMe
from view           import App

class Controller:
    ''' Initializes the app and handles the logic between the view and modules '''
    def __init__(self):
        # Load the database first to get the initial values
        self.db     = Db()

        # MuteMe device is optional
        try:
            self.muteme = MuteMe()
        except FileNotFoundError:
            self.muteme = 'no_device'
        except OSError:
            self.muteme = 'wrong_os'
        finally:
            self.muteme_available = isinstance(self.muteme, MuteMe)
            # Set default values, muteme or not
            self._muteme_color = 'noColor'
            self._muteme_mode = ''

        # Initialize view
        self.app = App(self)
        self.app.protocol('WM_DELETE_WINDOW', self._on_close)

    ###
    # App methods
    ###

    def run(self) -> None:
        ''' Start the app '''
        self.app.mainloop()

    def _on_close(self) -> None:
        ''' Clean up on close of app. '''
        if self.muteme_available:
            self.muteme.set_color('noColor')
        for timer in self.app.timers:
            timer.delete_timer()
        self.app.destroy()

    ###
    # Report methods
    ###

    def export_report(self, report:dict) -> None:
        ''' Export the report to a file '''
        
        # Rebuild report into tablular format
        report_list = []
        for category, data in report.items():
            for timer in data:
                report_list.append(timer)

        # Prompt user for file name
        filename = self.app.prompt_file_name()
        
        # Write to file
        with open(filename, 'w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=list(report_list[0].keys()))
            writer.writeheader()
            for timer in report_list:
                writer.writerow(timer)

    ###
    # MuteMe device methods
    ###
    @property
    def muteme_color(self) -> str:
        return self._muteme_color
    
    @muteme_color.setter
    def muteme_color(self, color:str):
        if self.muteme_available:
            if color not in self.muteme.colors:
                raise ValueError(f'Invalid color: {color}')
            
            # Hardware status may have changed, so catch the error and remove device
            try:
                self.muteme.set_color(color)
            except OSError:
                self.muteme = 'error'
                self.muteme_available = False

                if self.app.muteme_visible:
                    self.app.lights.destroy()
        # Track the color no matter so if the device is reconnected, it will be set
        self._muteme_color = color

    @property
    def muteme_mode(self) -> str:
        return self._muteme_mode
    
    @muteme_mode.setter
    def muteme_mode(self, mode:str):
        if self.muteme_available:
            valid_modes  = list(self.muteme.modes.keys()) + ['', 'strobe']
            if mode not in valid_modes:
                raise ValueError(f'Invalid mode: {mode}')
            
            # Hardware status may have changed, so catch the error and remove device
            try:
                if mode == 'strobe':
                    self._muteme_mode = mode
                    # Register the event loop handler with the device each time
                    # in case the device was disconnected
                    self.muteme.register_loop(self.app.after)
                    self.muteme.set_mode(mode)
                elif mode == self._muteme_mode:
                    # Toggle off if the mode is selected again
                    self._muteme_mode = ''
                    self.muteme.set_mode('')
                else:
                    self._muteme_mode = mode
                    self.muteme.set_mode(mode)
            except OSError:
                self.muteme_available = False
                self.muteme = 'error'

    def retry_muteme(self) -> None:
        ''' Allow the app to retry to connect to the muteme device when 
            the user clicks the MuteMe button'''
        try:
            self.muteme = MuteMe()
        except FileNotFoundError:
            self.muteme = 'no_device'

        except OSError:
            self.muteme = 'wrong_os'
        self.muteme_available = isinstance(self.muteme, MuteMe)

    def toggle_muteme_pwr(self) -> None:
        ''' Toggle the muteme device on and off '''
        self.muteme.on = not self.muteme.on

    ###
    # Wrap database methods
    ###
    def upsert_category(self, form:dict) -> int:
        return self.db.upsert_category(**form)

    def get_category_list(self):
        return self.db.get_all_categories()
    
    def get_root_category_list(self):
        return self.db.get_root_categories()

    def get_category(self, name:str):
        return self.db.get_category(name)

    def get_parent_category(self, id:int):
        return self.db.get_parent_category(id)

    def delete_category(self, id:int):
        self.db.delete_category(id)

    def insert_timer(self, category:str) -> int:
        cat = self.db.get_category(category)
        id = self.db.add_timer(cat['id'])
        return id
    
    def update_timer(self, id:int, duration:int=None, rest:int=None):
        if duration != None and rest != None:
            self.db.update_timer(id, duration=duration)
            self.db.update_timer(id, rest=rest)
        elif duration != None:
            self.db.update_timer(id, duration=duration)
        elif rest != None:
            self.db.update_timer(id, rest=rest)

    def finish_timer(self, id:int):
        self.db.finish_timer(id)

    def get_chained_timers(self, id:int):
        return self.db.get_chained_timers(id)

    def get_timer_report(self, period:str):
        # Could also have it by category, the db call is there, but not sure which is better
        return self.db.get_timer_report_by_date(period)

    def add_event(self, timer_id:int, event:str):
        self.db.add_event(timer_id, event)