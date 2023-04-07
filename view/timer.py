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
        self.exit     = False
        # Tk vars
        self.paused      = BooleanVar(value=True)
        self.category    = StringVar()
        self.timer_str   = StringVar(value='00:00')
        self.button_text = StringVar(value='Start')
        # Timer class vars
        self.color = 'green'
        self._time = 0 
        self.target_time = 0
        self.timer_chain = []

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
        category_list = [ x['name'] for x in self.controller.get_root_category_list()]
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

    def _reset_to_parent_timer(self):
        ''' Resets the timer to the parent timer '''
        category = self.controller.get_parent_category(self.parent_id)
        self.category.set(category['name'])
        self.seconds_left = category['duration']
        self.target_time  = category['duration']
        self.color = category['color']
        self.timer_label.configure(style=f'Timer.{self.color}.TLabel')
        self.chained_timers = self.controller.get_chained_timers(category['id'])


    def _category_selected(self, event):
        ''' Category selected '''
        category = self.controller.get_category(event)
        
        # This is selected from the input so it will be a parent
        self.parent_id = category['id']

        self.chained_timers = self.controller.get_chained_timers(category['id'])
        # Set the timer
        self.seconds_left = category['duration']
        self.target_time  = category['duration']
        # Set up the color
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
            if self.seconds_left == 0:
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
            # Absolut for stopwatch cause it counts up. 
            duration = abs(self.target_time - self.seconds_left)
            # Update db
            self.controller.add_event(self.id, 'pause')
            self.controller.update_timer(self.id, duration=duration)
            # Set the light to dim
            self.controller.muteme_mode = 'dim'

    def delete_timer(self):
        ''' Deletes the timer and updates db'''
        if self.started:
            duration = abs(self.target_time - self.seconds_left)
            self.controller.add_event(self.id, 'delete')
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
            self.controller.muteme_mode = '' 

        # Check if the timer is pause and throw it back on the loop
        if self.paused and self.seconds_left > 0:
            self.view.after(1000, self._timer_tick)
        
        elif self.seconds_left > 0:
            self.controller.muteme_color = self.color
            self.seconds_left = self.seconds_left - 1
            self.view.after(1000, self._timer_tick)
        
        elif len(self.chained_timers) > 0:
            # Mark the timer as finished
            self.controller.add_event(self.id, 'end')
            self.controller.update_timer(self.id, duration=self.target_time)
            self.controller.finish_timer(self.id)
        
            new_timer = self.chained_timers.pop(0)
            self.category.set(new_timer['name'])
                    # Set the timer
            self.seconds_left = new_timer['duration']
            self.target_time  = new_timer['duration']
            # Set up the color
            self.color = new_timer['color']
            self.timer_label.configure(style=f'Timer.{self.color}.TLabel')
            self.controller.muteme_color = self.color

            # Create new timer db entry
            self.id = self.controller.insert_timer(self.category.get())
            self.controller.add_event(self.id, 'start')
            self.view.after(1000, self._timer_tick)

        else:
            # Reset the timer back
            self.seconds_left = self.target_time
            self.started  = False
            self.button_text.set('Start')
            # Reset the label color
            self.timer_label.configure(style=f'Timer.{self.color}.TLabel')
            # Update db
            self.controller.add_event(self.id, 'end')
            self.controller.update_timer(self.id, duration=self.target_time)
            self.controller.finish_timer(self.id)
            # Turn off light
            self.controller.muteme_color = 'noColor'
            self.controller.muteme_mode  = ''

            # Reset the timer
            self._reset_to_parent_timer()

    def _destroy(self):
        ''' Destroy the timer items ''' 
        self.exit = True
        self.category_options.destroy()
        self.timer_label.destroy()
        self.start_btn.destroy()
        self.delete_btn.destroy()
