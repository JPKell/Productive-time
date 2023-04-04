from tkinter import StringVar, IntVar
from tkinter.ttk import Button, Label, OptionMenu, Combobox, Spinbox, Labelframe, Checkbutton, Frame

from settings import colors

# Todo: make the timer variables a property and have them format for 2 digits. 

class Manage(Labelframe):
    ''' Manages the timer categories '''

    def __init__(self, view):
        # Set up the frame
        super().__init__(view.frame, text='Categories', labelanchor='n')
        self.grid(row=50, column=0, columnspan=10, sticky='nsew', padx=5, pady=(8,8))
        
        # Grab app objects
        self.view = view
        self.controller = view.controller
        
        # Setup tkinter variables
        self.category      = StringVar()
        self.start_hours   = StringVar(value='00')
        self.start_minutes = StringVar(value='00')
        self.start_seconds = StringVar(value='00')
        self.end_hours     = StringVar(value='00')
        self.end_minutes   = StringVar(value='00')
        self.end_seconds   = StringVar(value='00')
        self.add_btn_txt   = StringVar(value='Add')
        self.color         = StringVar()
        self.color_list    = [*colors]
        self.pom_var       = IntVar()

        # Pomodoro row will appear as needed
        self.pomodoro_row = False

        self._build_ui()

    def _colon_lbl(self) -> Label:
        return Label(self, text=':', font=('Arial', 16))    
    
    def _build_ui(self) -> None:
        # Category list
        self.categories = Combobox(self, width=8, textvariable=self.category)
        self.categories.bind('<<ComboboxSelected>>', self._load_category)
        self._populate_categories()
        # Timer boxes

        numbers = [ f'{n:02}' for n in range(0,100) ]
        validate = (self.register(self._validate), '%P')
        common_settings = {'from_':0,'to':99, 'width':2, 'values':numbers, 'validate':'key', 'validatecommand':validate}
        start_hours   = Spinbox(self, textvariable=self.start_hours,   **common_settings)
        start_minutes = Spinbox(self, textvariable=self.start_minutes, **common_settings)
        start_seconds = Spinbox(self, textvariable=self.start_seconds, **common_settings)

        start_hours.bind('<FocusIn>', lambda e: self._on_spinbox(self.start_hours))
        start_minutes.bind('<FocusIn>', lambda e: self._on_spinbox(self.start_minutes))
        start_seconds.bind('<FocusIn>', lambda e: self._on_spinbox(self.start_seconds))
        start_hours.bind('<FocusOut>', lambda e: self._on_spinbox(self.start_hours))
        start_minutes.bind('<FocusOut>', lambda e: self._on_spinbox(self.start_minutes))
        start_seconds.bind('<FocusOut>', lambda e: self._on_spinbox(self.start_seconds))


        # Color select 
        self.color_list.insert(0, 'Red')
        self.colorselect = OptionMenu(self, self.color, *[ c.capitalize() for c in self.color_list])
        self.colorselect.config(width=4)
        # Pomodoro checkbox
        self.pom_check = Checkbutton(self, text='Pomodoro',variable=self.pom_var, command=self._toggle_pomodoro)
        # Buttons
        add_btn   = Button(self, textvariable=self.add_btn_txt, width=5, command=self._upsert_category)
        close_btn = Button(self, text='Del', width=2, command=self._delete_category)

        # Grid the widgets
        # Row 1
        self.categories.grid(row=0, column=0, columnspan=2, padx=5, sticky='we')
        start_hours.grid(row=0, column=2, sticky='we')
        self._colon_lbl().grid(row=0, column=3, sticky='we')
        start_minutes.grid(row=0, column=4, sticky='we')
        self._colon_lbl().grid(row=0, column=5, sticky='we')
        start_seconds.grid(row=0, column=6, padx=(0,5), sticky='we')
        
        # Row 3 
        self.colorselect.grid(row=2, column=0, padx=5, sticky='we')
        self.pom_check.grid(row=2, column=1, sticky='we')
        btn_settings = {'pady':3, 'sticky':'we'}
        add_btn.grid(row=2, column=3, columnspan=2, **btn_settings)
        close_btn.grid(row=2, column=5, columnspan=2, padx=5, **btn_settings)

        # Set the column weights
        self.columnconfigure(0, weight=1)

    def _toggle_pomodoro(self) -> None:
        ''' Toggles the pomodoro row on and off '''

        if self.pomodoro_row:
            self.pom_label.destroy()
            self.pom_hours.destroy()
            self.pom_minutes.destroy()
            self.pom_seconds.destroy()
            self.c1.destroy()
            self.c2.destroy()
            self.pomodoro_row = False
        else:
            # Widgets
            self.pom_label = Label(self, text='Rest time', font=('Arial', 12), anchor='e')
            numbers = [ f'{n:02}' for n in range(0,100) ]
            validate = (self.register(self._validate), '%P')
            common_settings = {'from_':0,'to':99, 'width':2, 'values':numbers, 'validate':'key', 'validatecommand':validate}

            self.pom_hours   = Spinbox(self, textvariable=self.end_hours,   **common_settings)
            self.pom_minutes = Spinbox(self, textvariable=self.end_minutes, **common_settings)
            self.pom_seconds = Spinbox(self, textvariable=self.end_seconds, **common_settings)

            self.pom_hours.bind('<FocusIn>',    lambda e: self._on_spinbox(self.end_hours))
            self.pom_minutes.bind('<FocusIn>',  lambda e: self._on_spinbox(self.end_minutes))
            self.pom_seconds.bind('<FocusIn>',  lambda e: self._on_spinbox(self.end_seconds))
            self.pom_hours.bind('<FocusOut>',   lambda e: self._on_spinbox(self.end_hours))
            self.pom_minutes.bind('<FocusOut>', lambda e: self._on_spinbox(self.end_minutes))
            self.pom_seconds.bind('<FocusOut>', lambda e: self._on_spinbox(self.end_seconds))

            # Grid
            self.pom_label.grid(row=1, column=0,columnspan=2, sticky='we', padx=(0,10), pady=10)
            self.pom_hours.grid(row=1, column=2, sticky='we')
            self.c1 = self._colon_lbl()
            self.c1.grid(row=1, column=3, sticky='we')
            self.pom_minutes.grid(row=1, column=4, sticky='we')
            self.c2 = self._colon_lbl()
            self.c2.grid(row=1, column=5, sticky='we')
            self.pom_seconds.grid(row=1, column=6, padx=(0,5), sticky='we')

            self.pomodoro_row = True


    def _upsert_category(self):
        duration = (int(self.start_hours.get()) * 3600) + \
                    (int(self.start_minutes.get()) * 60) + \
                    int(self.start_seconds.get())
        rest_duration = (int(self.end_hours.get()) * 3600) + \
                    (int(self.end_minutes.get()) * 60) + \
                    int(self.end_seconds.get())
        
        form = {
            'name': self.category.get(),
            'duration': duration,
            'rest': rest_duration,
            'color': self.color.get().lower(),
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
        self.color.set('Red')

    def _populate_categories(self):
        # Get the categories from the database
        categories = self.controller.get_category_list()
        # Get just the names
        categories = [category['name'] for category in categories]
        # Blank for the ability to add a new category
        categories.insert(0, '')
        self.categories['values'] = categories

    def _load_category(self, event=None):
        category = self.controller.get_category(self.category.get())
        if category:
            duration = category['duration']
            self.start_hours.set(f'{duration // 3600:02}')
            self.start_minutes.set(f'{(duration % 3600) // 60:02}')
            self.start_seconds.set(f'{duration % 60:02}')

            rest = category['rest']
            self.end_hours.set(f'{rest // 3600:02}')
            self.end_minutes.set(f'{(rest % 3600) // 60:02}')
            self.end_seconds.set(f'{rest % 60:02}')

            if rest > 0:
                self.pom_var.set('1')
                if not self.pomodoro_row:
                    self._toggle_pomodoro()
            else:
                self.pom_var.set('0')
                if self.pomodoro_row:
                    self.pom_label.destroy()
                    self.pom_hours.destroy()
                    self.pom_minutes.destroy()
                    self.pom_seconds.destroy()
                    self.c1.destroy()
                    self.c2.destroy()
                    self.pomodoro_row = False

            self.color.set(category['color'].capitalize())
            self.add_btn_txt.set('Update')
        else:
            self._reset_form()

    def _delete_category(self, event=None):
        self.controller.delete_category(self.category.get())
        self._reset_form()

    def _validate(self, value) -> bool:
        ''' Validates the input for the spinboxes '''
        if value.isdigit():
            if int(value) < 99 and int(value) >= 0:
                if len(value) > 2:
                    value = str(int(value)).zfill(2)
                return True
        elif value == '':
            return True
        return False
    
    def _on_spinbox(self, var:StringVar):
        ''' Clears the spinbox when the user clicks on it '''
        if var.get() == '00':
            var.set('')
        elif var.get() == '':
            var.set('00')
        elif len(var.get()) == 1:
            var.set(f'0{var.get()}')
        else:
            var.set(int(var.get()))