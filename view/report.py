from tkinter.ttk import Frame, Button, Labelframe, Treeview

class Report(Frame):
    
    def __init__(self, view):
        super().__init__(view.frame)
        self.view = view
        self.controller = view.controller
        self._column_setup()
        self._build_ui()

    def _column_setup(self):
        self.grid(row=50, column=0, columnspan=10, sticky='we')
        self.columnconfigure(0, weight=1)


    def _build_ui(self):
        row1 = Labelframe(self, text='Timer report',labelanchor='n',)
        row1.grid(row=0, column=0, sticky='we', pady=(8,8), padx=5)
        row1.columnconfigure(0, weight=1)
        row1.columnconfigure(1, weight=1)
        row1.columnconfigure(2, weight=1)
        row1.columnconfigure(3, weight=1)
        row1.columnconfigure(4, weight=1)

        week_btn  = Button(row1, text='Week',  width=5, command=lambda: self.select_range(7))
        month_btn = Button(row1, text='Month', width=5, command=lambda: self.select_range(30))
        year_btn  = Button(row1, text='Year',  width=5, command=lambda: self.select_range(365))
        all_btn   = Button(row1, text='All',   width=5, command=lambda: self.select_range('all'))
        export_btn = Button(row1, text='Export', width=5, command=lambda: self.controller.export_report(self.report))

        week_btn.grid(  row=0, column=0, sticky='we', padx=5, pady=5)
        month_btn.grid( row=0, column=1, sticky='we', padx=5, pady=5)
        year_btn.grid(  row=0, column=2, sticky='we', padx=5, pady=5)
        all_btn.grid(   row=0, column=3, sticky='we', padx=5, pady=5)
        export_btn.grid(row=0, column=4, sticky='we', padx=5, pady=5)

        self.report_tree = Treeview(row1, columns=('duration', 'rest', 'complete'))
        self.report_tree.heading('#0', text='')
        self.report_tree.heading('duration', text='Duration')
        self.report_tree.heading('rest', text='Rest')
        self.report_tree.heading('complete', text='Complete')

        self.report_tree.column('#0', width=100)
        self.report_tree.column('duration', width=50, anchor='c')
        self.report_tree.column('rest', width=50, anchor='c')
        self.report_tree.column('complete', width=20, anchor='c')

        self.report_tree.grid(row=1, column=0, columnspan=5, sticky='we', padx=5, pady=5)


    def update_report(self, report_dict:dict) -> None:
        ''' Adds the report results to the report treeview '''
        self.report = report_dict 
        # Clear the treeview
        self.report_tree.delete(*self.report_tree.get_children())
        # Loop through the report and populate the treeview
        for category, report in report_dict.items():
            # Calculate total duration and rest
            tot_duration = sum([record['duration'] for record in report if record['duration'] is not None])
            tot_rest = sum([record['rest'] for record in report if record['rest'] is not None])
            # Format the duration and rest
            tot_duration = f"{tot_duration//3600:02}:{(tot_duration % 3600) // 60:02}:{tot_duration % 60:02}"
            tot_rest = f"{tot_rest//3600:02}:{(tot_rest % 3600) // 60:02}:{tot_rest % 60:02}"

            tot_complete = sum([ record['complete'] for record in report ])

            self.report_tree.insert('', 'end', category, text=category, values=(tot_duration, tot_rest, tot_complete))
            for record in report:
                # Handle null values
                duration = record['duration'] if record['duration'] is not None else 0
                rest = record['rest'] if record['rest'] is not None else 0
                # Format the duration and rest
                duration = f"{duration//3600:02}:{(duration % 3600) // 60:02}:{duration % 60:02}"
                rest = f"{rest//3600:02}:{(rest % 3600) // 60:02}:{rest % 60:02}"

                self.report_tree.insert(category, 'end', text=record['start_time'][:10], values=(duration, rest, record['complete']))

    def select_range(self, int:str) -> None:
        ''' Selects the report range '''
        report = self.controller.get_timer_report(int)
        self.update_report(report)

    def export_report(self):
        ''' Exports the report to a csv file '''
        self.controller.export_report(self.report)
