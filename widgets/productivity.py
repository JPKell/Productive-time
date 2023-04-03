from tkinter import StringVar, IntVar
from tkinter.ttk import Button, Label, OptionMenu, Combobox, Spinbox, LabelFrame, Checkbutton, Frame

from settings import colors

class Productivity(LabelFrame):
    def __init__(self, view):
        super().__init__(view.frame, text='Categories', labelanchor='n')
        self.grid(row=50, column=0, columnspan=10, sticky='nsew', padx=5, pady=(8,8))
        self.view = view
        self.controller = view.controller

        self.category = StringVar()
        self.start_hours    = StringVar(value='00')
        self.start_minutes  = StringVar(value='00')
        self.start_seconds  = StringVar(value='00')
        self.end_hours    = StringVar(value='00')
        self.end_minutes  = StringVar(value='00')
        self.end_seconds  = StringVar(value='00')
        self.add_btn_txt = StringVar(value='Add')
        self.color    = StringVar(value='red')
        self.color_list = [*colors]

        self.pomodoro_row = None
        self.pom_var = IntVar()

        self._build_ui()
        

    def _build_ui(self):
        # Category list
        self.categories = Combobox(self, width=8, textvariable=self.category)
        self.categories.bind('<<ComboboxSelected>>', self._load_category)
        self._populate_categories()
        # Timer boxes
        start_hours   = Spinbox(self, from_=0, to=24, width=2, textvariable=self.start_hours)
        colon = Label(self, text=':', font=('Arial', 16))
        start_minutes = Spinbox(self, from_=0, to=60, width=2, textvariable=self.start_minutes)
        colon2 = Label(self, text=':', font=('Arial', 16))
        start_seconds = Spinbox(self, from_=0, to=60, width=2, textvariable=self.start_seconds)


        self.color_list.insert(0, 'red')
        self.colorselect = OptionMenu(self, self.color, *self.color_list)
        self.colorselect.config(width=4)

        self.pom_check = Checkbutton(self, text='Pomodoro',variable=self.pom_var, command=self._toggle_pomodoro)
        add_btn = Button(self, textvariable=self.add_btn_txt, width=5, command=self._upsert_category)
        close_btn = Button(self, text='Del', width=2, command=self._delete_category)

        # Grid the widgets
        # Row 1
        self.categories.grid(row=0, column=0, columnspan=2, padx=5, sticky='we')
        start_hours.grid(row=0, column=2, sticky='we')
        colon.grid(row=0, column=3, sticky='we')
        start_minutes.grid(row=0, column=4, sticky='we')
        colon2.grid(row=0, column=5, sticky='we')
        start_seconds.grid(row=0, column=6, padx=(0,5), sticky='we')
        
        # Row 3 
        self.colorselect.grid(row=2, column=0, padx=5, sticky='we')
        self.pom_check.grid(row=2, column=1, sticky='we')

        btn_settings = {'pady':3, 'sticky':'we'}
        add_btn.grid(row=2, column=3, columnspan=2, **btn_settings)
        close_btn.grid(row=2, column=5, columnspan=2, padx=5, **btn_settings)

        # Set the column weights
        self.columnconfigure(0, weight=1)

    def _toggle_pomodoro(self):

        if self.pomodoro_row:
            self.pomodoro_row.destroy()
            self.pomodoro_row = None
        else:
            self.pomodoro_row = Frame(self)
            self.pomodoro_row.columnconfigure(0, weight=1)

            label = Label(self.pomodoro_row, text='Rest time', font=('Arial', 12), anchor='e')
            end_hours   = Spinbox(self.pomodoro_row, from_=0, to=24, width=2, textvariable=self.end_hours)
            colon3 = Label(self.pomodoro_row, text=':', font=('Arial', 16))
            end_minutes = Spinbox(self.pomodoro_row, from_=0, to=60, width=2, textvariable=self.end_minutes)
            colon4 = Label(self.pomodoro_row, text=':', font=('Arial', 16))
            end_seconds = Spinbox(self.pomodoro_row, from_=0, to=60, width=2, textvariable=self.end_seconds)

            self.pomodoro_row.grid(row=1, column=0, columnspan=7, sticky='we')
            label.grid(row=0, column=0,columnspan=2, sticky='we', padx=(0,10))
            end_hours.grid(row=0, column=2, sticky='we')
            colon3.grid(row=0, column=3, sticky='we')
            end_minutes.grid(row=0, column=4, sticky='we')
            colon4.grid(row=0, column=5, sticky='we')
            end_seconds.grid(row=0, column=6, padx=(0,5), sticky='we')


    def _upsert_category(self):
        start_hours   = int(self.start_hours.get())
        start_minutes = int(self.start_minutes.get())
        start_seconds = int(self.start_seconds.get())
        duration = (start_hours * 3600) + (start_minutes * 60) + start_seconds

        rest_hours   = int(self.end_hours.get())
        rest_minutes = int(self.end_minutes.get())
        rest_seconds = int(self.end_seconds.get())
        rest_duration = (rest_hours * 3600) + (rest_minutes * 60) + rest_seconds

        form = {
            'name': self.category.get(),
            'duration': duration,
            'rest': rest_duration,
            'color': self.color.get(),
            'active': 1
        }

        if self.category.get() != '':
            self.controller.upsert_category(form)
            self._reset_form()

    def _reset_form(self):
        self._populate_categories()
        self.category.set('')
        self.start_hours.set('00')
        self.start_minutes.set('00')
        self.start_seconds.set('00')
        self.end_hours.set('00')
        self.end_minutes.set('00')
        self.end_seconds.set('00')
        self.pom_var.set(0)
        if self.pomodoro_row:
            self.pomodoro_row.destroy()
            self.pomodoro_row = None
        self.color.set('red')

    def _populate_categories(self):
        categories = self.controller.get_category_list()
        categories = [category['name'] for category in categories]
        categories.insert(0, '')
        self.categories['values'] = categories

    def _load_category(self, event=None):
        category = self.controller.get_category(self.category.get())
        if category:
            duration = category['duration']
            self.start_hours.set(str(duration // 3600))
            self.start_minutes.set(str((duration % 3600) // 60))
            self.start_seconds.set(str(duration % 60))

            rest = category['rest']
            self.end_hours.set(str(rest // 3600))
            self.end_minutes.set(str((rest % 3600) // 60))
            self.end_seconds.set(str(rest % 60))

            if rest > 0:
                self.pom_var.set('1')
                self.pomodoro_row = None
                self._toggle_pomodoro()
            else:
                self.pom_var.set('0')
                if self.pomodoro_row:
                    self.pomodoro_row.destroy()
                    self.pomodoro_row = None

            self.color.set(category['color'])
            self.add_btn_txt.set('Update')
        else:
            self._reset_form()

    def _delete_category(self, event=None):
        self.controller.delete_category(self.category.get())
        self._reset_form()