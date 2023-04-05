from tkinter import StringVar, IntVar
from tkinter.ttk import Button, Label, OptionMenu, Combobox, Spinbox, Labelframe, Checkbutton, Frame, Entry

from settings import colors, chained_timer_name

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
        # Tkinter variables
        self.add_btn_txt   = StringVar(value='Add')
        self.del_btn_txt   = StringVar(value='Delete')
        # Category timer stack
        self.stack = []
        self.undo_stack = []
        self.delete_armed = False

        self._build_ui()

 
    def _build_ui(self) -> None:
        self.columnconfigure(0, weight=1)

        self._build_menu_row()
        self._build_timer_row()

    def _build_menu_row(self) -> None:
        frm = Frame(self)
        frm.columnconfigure(0, weight=1)
        frm.columnconfigure(1, weight=1)
        frm.columnconfigure(2, weight=1)
        frm.columnconfigure(3, weight=1)
        frm.columnconfigure(4, weight=1)


        chain_btn = Button(frm, text='Chain timer', width=8, command=self._build_timer_row)
        unchain_btn = Button(frm, text='Delete last', width=8, command=self._pop_timer_row)
        add_btn   = Button(frm, textvariable=self.add_btn_txt, style='green.TButton', width=5, command=self._upsert_category)
        close_btn = Button(frm, textvariable=self.del_btn_txt, width=6, style='red.TButton', command=self._delete_category)

        frm.grid(row=99, column=0, columnspan=10, sticky='we', padx=5, pady=5)
        btn_settings = {'pady':3, 'sticky':'we'}
        chain_btn.grid(  row=0, column=0, padx=5, **btn_settings)
        unchain_btn.grid(row=0, column=1, **btn_settings)
        add_btn.grid(    row=0, column=4, **btn_settings)
        close_btn.grid(  row=0, column=5, padx=5, **btn_settings)

    def _build_timer_row(self, event=None) -> None:
        ''' Timers add themselves to the stack '''
        if len(self.undo_stack) > 0:
            old_row = self.undo_stack.pop()
            old_row.grid(row=len(self.stack), column=0, sticky='we', padx=5, pady=5)
            self.stack.append(old_row)
        else:
            new_row = TimerRow(self, self.stack, self.controller)
            new_row.bind('<<CategorySelected>>', lambda event: self._load_chained_timers(new_row))
            new_row.build()

    def _load_chained_timers(self, parent_timer) -> None:
        children = self.controller.get_chained_timers(parent_timer.id)
        for child in children:
            new_row = TimerRow(self, self.stack, self.controller)
            new_row.id = child['id']
            new_row.parent_id = child['parent_id']
            new_row.category.set(child['name'])
            new_row.hours.set(f"{child['duration'] // 3600:02}")
            new_row.minutes.set(f"{(child['duration'] % 3600) // 60:02}")
            new_row.seconds.set(f"{child['duration'] % 60:02}")
            new_row.color.set(child['color'])
            new_row.build()
            new_row.colorselect.set_menu(child['color'].capitalize(), *[ c.capitalize() for c in colors if c != 'noColor'])

    def _pop_timer_row(self, event=None) -> None:
        if len(self.stack) > 1:
            old_row = self.stack.pop()
            old_row.grid_forget()
            self.undo_stack.append(old_row)

    def _delete_category(self, event=None):
        ''' Delete the category from the database '''
        if self.delete_armed:
            self.controller.delete_category(self.stack[0].id)
            self.delete_armed = False
            self.del_btn_txt.set('Delete')
            self.add_btn_txt.set('Add')
            for timer in self.stack:
                timer.destroy()
            self.stack = []
            for timer in self.undo_stack:
                timer.destroy()
            self.undo_stack = []
            self._build_timer_row()
        else:
            self.delete_armed = True
            self.del_btn_txt.set('Really?')
            



    def _upsert_category(self, event=None):
        ''' Upsert the category into the database '''
        # Clear any children first. An existing timer will have an Id. New will not
        if self.stack[0].id is not None:
            children = self.controller.get_chained_timers(self.stack[0].id)

            orphans = [ x for x in children if x['id'] not in [ y.id for y in self.stack ] ]
            for orphan in orphans:
                self.controller.delete_category(orphan['id'])

        parent_id = None
        for timer in self.stack:
            if parent_id is None:
                parent_id = timer.update_db()
            else:
                timer.parent_id = parent_id
                timer.update_db()

        # Delete the stack
        for timer in self.stack:
            timer.destroy()
        self.stack = []
        for timer in self.undo_stack:
            timer.destroy()
        self.undo_stack = []
        self._build_timer_row()
    


class TimerRow(Frame):
    ''' A row of widgets for creating timer categories '''
    def __init__(self, parent:Frame, stack:list, controller):
        # Set up the frame
        super().__init__(parent)
        self.columnconfigure(0, weight=1)
        self.grid(row=len(stack), column=0, columnspan=10, sticky='we', padx=5, pady=5)
        # Grab app objects
        self.controller = controller
        self.parent = parent
        # Set up meta data
        # The whole reason for the stack in the class is to let the first row
        # be the parent row. So the timer is updated into the db it can populate 
        # the parent_id for all the child rows.  
        self.stack = stack
        self.sort  = len(stack)
        self.id    = None
        self.parent_id = None

        # Setup tkinter variables
        self.category   = StringVar()
        self.hours      = StringVar(value='00')
        self.minutes    = StringVar(value='00')
        self.seconds    = StringVar(value='00')
        self.color      = StringVar()
        self.color_list = [*colors]

    def __del__(self):
        # This may have already been destroyed
        try:
            self.destroy()
        except:
            ...

    def build(self) -> None:
        self._build_timer_row()
    
    def _build_timer_row(self) -> None:
        # Category list
        if len(self.stack) == 0:
            self.categories = Combobox(self, width=8, textvariable=self.category)
            self.categories.bind('<<ComboboxSelected>>', self._load_category)
            self._populate_categories()
        else:
            if self.category.get() == '':
                self.category.set(f"{chained_timer_name} {len(self.stack)}")
            self.categories = Entry(self, width=8, textvariable=self.category)

        # Add self to the stack since this can set off a chain reaction
        # of building more rows if there are children
        self.stack.append(self)

        validate = (self.parent.register(self._validate), '%P')

        common_settings = {'font':'Arial 14 bold', 'width':2, 'validate':'key', 'validatecommand':validate}
        hours   = Entry(self, textvariable=self.hours,   **common_settings)
        minutes = Entry(self, textvariable=self.minutes, **common_settings)
        seconds = Entry(self, textvariable=self.seconds, **common_settings)

        hours.bind('<FocusIn>', lambda e: self._on_focus(self.hours))
        minutes.bind('<FocusIn>', lambda e: self._on_focus(self.minutes))
        seconds.bind('<FocusIn>', lambda e: self._on_focus(self.seconds))
        hours.bind('<FocusOut>', lambda e: self._on_focus(self.hours))
        minutes.bind('<FocusOut>', lambda e: self._on_focus(self.minutes))
        seconds.bind('<FocusOut>', lambda e: self._on_focus(self.seconds))

        # Color select 
        self.color_list = [ c for c in self.color_list if c != 'noColor' ]
        self.color_list.insert(0, 'Red')
        self.colorselect = OptionMenu(self, self.color, *[ c.capitalize() for c in self.color_list])
        self.colorselect.config(width=8)

        # Grid the widgets
        self.categories.grid(row=0, column=0, padx=5, sticky='we')
        hours.grid(row=0, column=2, padx=(5,0), pady=0, sticky='we')
        Label(self, text=':', font=('Arial', 16)).grid(row=0, column=3, sticky='we')
        minutes.grid(row=0, column=4, sticky='we')
        Label(self, text=':', font=('Arial', 16)).grid(row=0, column=5, sticky='we')
        seconds.grid(row=0, column=6, padx=(0,5), sticky='we')

        self.colorselect.grid(row=0, column=7, padx=5, sticky='we')

    def _on_focus(self, var:StringVar):
        ''' Clears the spinbox when the user clicks on it '''
        if var.get() == '00':
            var.set('')
        elif var.get() == '':
            var.set('00')
        elif len(var.get()) == 1:
            var.set(f'0{var.get()}')
        else:
            var.set(int(var.get()))

    def _load_category(self, event=None):
        category = self.controller.get_category(self.category.get())
        
        # Clear the stack
        while len(self.stack) > 1:
            self.stack.pop().destroy()
        self.parent.undo_stack = []

        # We are starting with a fresh form
        if category:
            self.id = category['id']
            duration = category['duration']
            self.hours.set(f'{duration // 3600:02}')
            self.minutes.set(f'{(duration % 3600) // 60:02}')
            self.seconds.set(f'{duration % 60:02}')
            self.color.set(category['color'].capitalize())
            self.parent.add_btn_txt.set('Update')
            # If we are building the form from fresh. 
            if len(self.stack) == 0:
                self._build_timer_row()     
            # Signal so any children can be added
            self.event_generate('<<CategorySelected>>')
        else:
            self.parent.add_btn_txt.set('Add')
            self._reset_form()
            

    def _populate_categories(self):
        # Get the categories from the database
        categories = self.controller.get_root_category_list()
        # Get just the names
        categories = [category['name'] for category in categories]
        # Blank for the ability to add a new category
        categories.insert(0, '')
        self.categories['values'] = categories


    def _reset_form(self):
        self.category.set('')
        self.hours.set('00')
        self.minutes.set('00')
        self.seconds.set('00')
        self.color.set('Red')
        # self._populate_categories()

    def _validate(self, value) -> bool:
        ''' Validates the input for the entry boxes '''
        if value.isdigit():
            if int(value) < 99 and int(value) >= 0:
                if len(value) > 2:
                    value = str(int(value)).zfill(2)
                return True
        elif value == '':
            return True
        return False
    
    def update_db(self):
        duration = (int(self.hours.get()) * 3600) + (int(self.minutes.get()) * 60) + int(self.seconds.get())

        form = {
            'parent_id': self.parent_id,
            'sort': self.sort,
            'name': self.category.get(),
            'duration': duration,
            'color': self.color.get().lower(),
            'active': 1
        }

        if self.id is not None:
            form['id'] = self.id

        if self.category.get() != '':
            # Add the category to the database
            self.id = self.controller.upsert_category(form)

            self._reset_form()

            return self.id
        
