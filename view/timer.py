from tkinter import StringVar, BooleanVar
from tkinter.ttk import Button, Label, OptionMenu

class Timer:
    def __init__(self, view, row:int):
        # Get the app objects
        self.frame = view.frame
        self.view = view
        self.controller = view.controller
        # Timer metadata
        self.row = row
        self.id = 0
        # Flags         
        self.started  = False
        self.on_break = False
        self.exit     = False
        # Tk vars
        self.paused      = BooleanVar(value=True)
        self.category    = StringVar()
        self.timer_str   = StringVar()
        self.button_text = StringVar(value='Start')
        # Timer class vars
        self.color = 'green'
        self.seconds_left = 0
        self.productive_time = 0
        self.rest_time = 0
        self._time = 0 

        self._build_ui()

    @property
    def seconds_left(self):
        return self._time
    
    @seconds_left.setter
    def seconds_left(self, value):
        self._time = value
        hours   = value // 3600
        minutes = (value - (hours * 3600)) // 60
        seconds = value % 60

        if hours == 0:
            self.timer_str.set(f"{minutes:02}:{seconds:02}")
        else:
            self.timer_str.set(f"{hours:02}:{minutes:02}:{seconds:02}")


    def _build_ui(self):
        ''' Builds a new timer widget '''
        # Set up the widgets
        category_list = [ x['name'] for x in self.controller.get_category_list()]
        category_list.insert(0, 'Stopwatch')
        self.category_options = OptionMenu(self.frame, self.category, *category_list, command=self._category_selected)
        self.category_options.config(width=10)
        self.category_options.bind()

        self.timer_label = Label(self.frame, textvariable=self.timer_str, style='Timer.TLabel',font=('Arial', 24, "bold"),  anchor='center',width=10)
        self.start_btn   = Button(self.frame, textvariable=self.button_text, command=self.start_timer)
        self.delete_btn  = Button(self.frame, text='X', width=2, command=lambda: self.view.remove_timer(self), style='red.TButton')

        # Grid the widgets
        self.grid_widgets(self.row)

    def grid_widgets(self, row:int):
        ''' Grids the widgets '''
        # Pack the widgets
        btn_settings = {'pady':3, 'padx':5, 'sticky':'we'}
        self.category_options.grid(row=row, column=0, columnspan=3,**btn_settings)
        self.timer_label.grid(row=row, column=3, columnspan=4, **btn_settings,)
        self.start_btn.grid(row=row, column=7, columnspan=2,**btn_settings)
        self.delete_btn.grid(row=row, column=9,  **btn_settings)

    def _category_selected(self, event):
        ''' Category selected '''
        category = self.controller.get_category(event)
        # Set the productive time and the rest time
        self.productive_time = category['duration']
        self.rest_time       = category['rest']
        # Set the timer to the productive time
        self.seconds_left    = self.productive_time
        self.color = category['color']
        self.timer_label.configure(style=f'Timer.{self.color}.TLabel')
        self.category.set(event)

    def start_timer(self):
        ''' Starts the timer and pauses and resumes as needed '''
        if not self.started:
            # Set the label and variables
            self.button_text.set('Pause')
            self.started = True
            self.paused = False
            # Replace category options with a label
            self.category_options.destroy()
            self.category_options = Label(self.frame, textvariable=self.category, width=10, font=('Arial', 12, 'bold'), anchor='center')
            self.category_options.grid(row=self.row, column=0, columnspan=3, padx=5, pady=3, sticky='we')
            # Update db
            self.id = self.controller.insert_timer(self.category.get())
            self.controller.add_event(self.id, 'start')
            # Turn on MuteMe if it exists
            if self.controller.muteme_available:
                self.controller.muteme.on = True

            # Start the timer
            if self.productive_time == 0:
                self._stopwatch_tick()
            else:
                self._timer_tick()

        elif self.paused:
            # Set the label and variables
            self.button_text.set('Pause')
            self.paused = False
            # Update db
            self.controller.add_event(self.id, 'resume')
            # Set the light to normal
            self.controller.muteme_mode = ''
        elif not self.paused:
            # Set the label and variables
            self.button_text.set('Resume')
            self.paused = True
            # Update db
            self.controller.add_event(self.id, 'pause')
            if self.on_break:
                duration = self.rest_time - self.seconds_left
                self.controller.update_timer(self.id, rest=duration)
            else:
                # Absolut for stopwatch cause it counts up. 
                duration = abs(self.productive_time - self.seconds_left)
                self.controller.update_timer(self.id, duration=duration)
            # Set the light to dim
            self.controller.muteme_mode = 'dim'

    def delete_timer(self):
        ''' Deletes the timer and updates db'''
        if self.started:
            self.controller.add_event(self.id, 'delete')
            if self.on_break:
                duration = self.rest_time - self.seconds_left
                self.controller.update_timer(self.id, rest=duration)
            else:
                # Absolut for stopwatch cause it counts up. 
                duration = abs(self.productive_time - self.seconds_left)
                self.controller.update_timer(self.id, duration=duration)
        self._destroy()

    def _stopwatch_tick(self):
        ''' Stopwatch tick function '''
        if self.exit:
            return
        # Check if the timer is pause and throw it back on the loop
        self.controller.muteme_color = self.color
        if self.paused and self.seconds_left > 0:
            self.view.after(1000, self._stopwatch_tick)
        else:
            self.seconds_left = self.seconds_left + 1
            self.view.after(1000, self._stopwatch_tick)

    def _timer_tick(self):
        ''' Timer tick function '''
        if self.exit:
            return

        if self.seconds_left == 30:
            self.controller.muteme_mode = 'slow'
        elif self.seconds_left == 15:
            self.controller.muteme_mode = 'fast'
        elif self.seconds_left == 3:
            self.controller.muteme_mode = 'strobe'
        elif self.seconds_left == 0:

            ... # Set back to previous light 

        # Check if the timer is pause and throw it back on the loop
        if self.paused and self.seconds_left > 0:
            self.view.after(1000, self._timer_tick)
        
        elif self.seconds_left > 0:
            color = 'green' if self.on_break else self.color
            self.controller.muteme_color = color
            self.seconds_left = self.seconds_left - 1
            self.view.after(1000, self._timer_tick)
        
        # 0 Seconds left on timer
        elif not self.on_break:
            self.on_break = True
            # MuteMe color
            self.controller.muteme_color = 'green'
            self.controller.muteme_mode = ''
            # Timer color
            self.timer_label.configure(style='green.TLabel')
            
            self.seconds_left = self.rest_time

            self.controller.add_event(self.id, 'break')
            self.controller.update_timer(self.id, duration=self.productive_time)
            self.view.after(1000, self._timer_tick)
        else:
            # Reset the timer back
            self.seconds_left = self.productive_time
            self.on_break = False
            self.started  = False
            # Reset the label color
            self.timer_label.configure(style=f'Timer.{self.color}.TLabel')
            # Update db
            self.controller.add_event(self.id, 'end')
            self.controller.update_timer(self.id, rest=self.rest_time)
            self.controller.finish_timer(self.id)
            # Turn off light
            self.controller.muteme_color = 'noColor'
            self.controller.muteme_mode  = ''

    def _destroy(self):
        ''' Destroy the timer items ''' 
        self.exit = True
        self.category_options.destroy()
        self.timer_label.destroy()
        self.start_btn.destroy()
        self.delete_btn.destroy()
