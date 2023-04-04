from tkinter.ttk import Button


class Menu:
    def __init__(self, view):
        self.frame = view.frame
        self.view = view
        self.controller = view.controller
        self._build_ui()

    def _build_ui(self):
        # Buttons
        self.report_btn    = Button(self.frame, text='Report', width=15, command=self.view.report_widget)
        self.new_timer_btn = Button(self.frame, text='New timer', command=self.view.timer_widget)
        self.manage_btn    = Button(self.frame, text='Manage',    command=self.view.manage_widget)
        self.setup_btn     = Button(self.frame, text='Setup', width=5, command=self.view.lights_widget)

        # Grid the buttons
        btn_settings = {'padx':5, 'pady':(3,8), 'sticky':'we'}
        self.report_btn.grid(   row=99, column=0, columnspan=3, **btn_settings)
        self.new_timer_btn.grid(row=99, column=3, columnspan=4, **btn_settings)
        self.manage_btn.grid(   row=99, column=7, columnspan=2, **btn_settings)
        self.setup_btn.grid(    row=99, column=9, **btn_settings)
