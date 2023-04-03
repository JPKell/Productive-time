from tkinter.ttk import Frame, Button, Labelframe

class Lights(Frame):
    
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
        row2.columnconfigure(4, weight=1)
        row2.columnconfigure(5, weight=1)
        row2.columnconfigure(6, weight=1)
        row2.columnconfigure(7, weight=1)

        common = { 'width': 4}

        # Row 1
        dim_btn = Button(row1, text="Dim", command=lambda: self._set_light_mode('dim'), **common)
        slow_btn = Button(row1, text="Slow", command=lambda: self._set_light_mode('slow'), **common)
        fast_btn = Button(row1, text="Fast", command=lambda: self._set_light_mode('fast'), **common)
        none_btn = Button(row1, text="Strobe", command=lambda: self._set_light_mode('strobe'), **common)

        btn_grid = {'sticky': 'we', 'padx': 2, 'pady': 3}
        dim_btn.grid( row=0, column=0, **btn_grid)
        slow_btn.grid(row=0, column=1, **btn_grid)
        fast_btn.grid(row=0, column=2, **btn_grid)
        none_btn.grid(row=0, column=3, **btn_grid)

        # Row 2
        red_btn    = Button(row2, text="Red",    command=lambda: self._set_light_color('red'), **common)
        yellow_btn = Button(row2, text="Yellow", command=lambda: self._set_light_color('yellow'), **common)
        green_btn  = Button(row2, text="Green",  command=lambda: self._set_light_color('green'), **common)
        cyan_btn   = Button(row2, text="Cyan",   command=lambda: self._set_light_color('cyan'), **common)
        blue_btn   = Button(row2, text="Blue",   command=lambda: self._set_light_color('blue'), **common)
        purple_btn = Button(row2, text="Purple", command=lambda: self._set_light_color('purple'), **common)
        white_btn  = Button(row2, text="White",  command=lambda: self._set_light_color('white'), **common)
        black_btn  = Button(row2, text="Off",    command=lambda: self._set_light_color('noColor'), **common)

        red_btn.grid(row=0, column=0, **btn_grid)
        yellow_btn.grid(row=0, column=1, **btn_grid)
        green_btn.grid(row=0, column=2, **btn_grid)
        cyan_btn.grid(row=0, column=3, **btn_grid)
        blue_btn.grid(row=0, column=4, **btn_grid)
        purple_btn.grid(row=0, column=5, **btn_grid)
        white_btn.grid(row=0, column=6, **btn_grid)
        black_btn.grid(row=0, column=7, **btn_grid)


    def _set_light_color(self, color:str):
        self.controller.light_color = color

    def _set_light_mode(self, effect:str):
        self.controller.light_mode = effect

        # rb_btn = Button(row1, text="Rainbow", command= print, **common)
        # sb_btn = Button(row1, text="Strobe", command=lambda: print('strobe'), **common)
