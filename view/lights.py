from tkinter.ttk import Frame, Button, Labelframe, Label

class Lights(Frame):
    ''' The lights widget. This gives the user the ability to control the
        MuteMe device. It is only available if the device is connected to the
        system. If the device is not connected, the widget will display a 
        message to the user.'''
    
    def __init__(self, view):
        # Initialize the superclass
        super().__init__(view.frame)
        self.grid(row=50, column=0, columnspan=10, sticky='we')
        self.columnconfigure(0, weight=1)
        # Grab app objects
        self.view = view
        self.controller = view.controller
        # Build the UI
        if self.controller.muteme_available:
            self._build_ui()
        else:
            self._show_no_device()

    def _show_no_device(self) -> None:
        ''' If the device is not connected, this method will display a message to the user. '''
        # Try the device again just incase it was connected after the app started
        self.controller.retry_muteme()

        # If the device has been found, rebuild the UI
        if not isinstance(self.controller.muteme, str):
            self._build_ui()
            return
        
        # Else show the message
        elif self.controller.muteme == 'no_device':
            title = 'No device'
            txt = 'No MuteMe device found on your system. Thats okay, you can still use the app'
        elif self.controller.muteme == 'wrong_os':
            title = 'Wrong OS'
            txt = 'MuteMe integration is only available for Linux at the moment. Sorry!'
        elif self.controller.muteme == 'error':
            title = 'Error'
            txt = 'There was an error connecting to the MuteMe device. Check the device and try again'

        # Build and pack widgets
        self.frm = Labelframe(self, text=title, labelanchor='n')
        self.frm.grid(row=0, column=0, sticky='nswe', pady=(8,8), padx=5)
        self.frm.columnconfigure(0, weight=1)
        lbl = Label(self.frm, text=txt, wraplength=355,justify='center',anchor='center',)
        lbl.grid(row=0, column=0, sticky='nswe', pady=(8,8), padx=5)



    def _build_ui(self):
        ''' Build the UI for the lights widget. '''

        # Set up rows
        row1 = Labelframe(self, text='Modes',labelanchor='n',)
        row1.grid(row=0, column=0, sticky='we', pady=(8,8), padx=5)
        row1.columnconfigure(0, weight=1)
        row1.columnconfigure(1, weight=1)
        row1.columnconfigure(2, weight=1)
        row1.columnconfigure(3, weight=1)
        row2 = Labelframe(self, text='Colors', labelanchor='n')
        row2.grid(row=1, column=0, sticky='we', pady=(0,10), padx=5)
        row2.columnconfigure(0, weight=1)
        row2.columnconfigure(1, weight=1)
        row2.columnconfigure(2, weight=1)
        row2.columnconfigure(3, weight=1)

        # Button settings
        common = { 'width': 4}
        btn_grid = {'sticky': 'we', 'padx': 2, 'pady': 3}

        # Row 1
        dim_btn  = Button(row1, text="Dim",    command=lambda: self._set_muteme_mode('dim'),    **common)
        slow_btn = Button(row1, text="Slow",   command=lambda: self._set_muteme_mode('slow'),   **common)
        fast_btn = Button(row1, text="Fast",   command=lambda: self._set_muteme_mode('fast'),   **common)
        none_btn = Button(row1, text="Strobe", command=lambda: self._set_muteme_mode('strobe'), **common)
        dim_btn.grid( row=0, column=0, **btn_grid)
        slow_btn.grid(row=0, column=1, **btn_grid)
        fast_btn.grid(row=0, column=2, **btn_grid)
        none_btn.grid(row=0, column=3, **btn_grid)

        # Row 2
        red_btn    = Button(row2, text="Red",    style='red.TButton',    command=lambda: self._set_muteme_color('red'),     **common)
        yellow_btn = Button(row2, text="Yellow", style='yellow.TButton', command=lambda: self._set_muteme_color('yellow'),  **common)
        green_btn  = Button(row2, text="Green",  style='green.TButton',  command=lambda: self._set_muteme_color('green'),   **common)
        cyan_btn   = Button(row2, text="Cyan",   style='cyan.TButton',   command=lambda: self._set_muteme_color('cyan'),    **common)
        blue_btn   = Button(row2, text="Blue",   style='blue.TButton',   command=lambda: self._set_muteme_color('blue'),    **common)
        purple_btn = Button(row2, text="Purple", style='purple.TButton', command=lambda: self._set_muteme_color('purple'),  **common)
        white_btn  = Button(row2, text="White",  style='white.TButton',  command=lambda: self._set_muteme_color('white'),   **common)
        black_btn  = Button(row2, text="Off",    style='black.TButton',  command=lambda: self._set_muteme_color('off'),     **common)
        red_btn.grid(   row=0, column=0, **btn_grid)
        yellow_btn.grid(row=0, column=1, **btn_grid)
        green_btn.grid( row=0, column=2, **btn_grid)
        cyan_btn.grid(  row=0, column=3, **btn_grid)
        blue_btn.grid(  row=1, column=0, **btn_grid)
        purple_btn.grid(row=1, column=1, **btn_grid)
        white_btn.grid( row=1, column=2, **btn_grid)
        black_btn.grid( row=1, column=3, **btn_grid)


    def _set_muteme_color(self, color:str) -> None:
        if color == 'off':
            self.controller.toggle_muteme_pwr()
        else:
            self.controller.muteme_color = color

    def _set_muteme_mode(self, effect:str) -> None:
        self.controller.muteme_mode = effect
