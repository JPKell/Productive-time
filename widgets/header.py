from tkinter.ttk import Frame, Button


class Header:
    def __init__(self, view):
        self.frame = view.frame
        self.view = view
        self.controller = view.controller
        self._build_ui()

    def _build_ui(self):
        ''' Builds the header of the app '''

        # Buttons
        self.productivity_btn = Button(self.frame, text='Productivity', width=15, command=self.view.productivity_widget)
        self.new_timer_btn = Button(self.frame, text='New timer', command=self.view.timer_widget)
        self.lights_btn = Button(self.frame, text='Lights', width=15, command=self.view.lights_widget)

        btn_settings = {'padx':5, 'pady':3, 'sticky':'we'}
        # Grid the buttons
        self.productivity_btn.grid(row=0, column=0, columnspan=3, **btn_settings)
        self.new_timer_btn.grid(row=0, column=3, columnspan=4, **btn_settings)
        self.lights_btn.grid(row=0, column=7, columnspan=3, **btn_settings)
