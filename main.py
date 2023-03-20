import tkinter as tk

from device import Emetum

black = '#220505'

dev = Emetum()

strobe_on = False
def strobe(color='white'):
    global strobe_on
    strobe_on = True
    _strobe(color)     

def _strobe(color='white', on=True):
    global strobe_on
    if strobe_on:
        if not on:
            dev.set_color('noColor')
        else:
            dev.set_color(color)
        on = not on
        app.after(30, _strobe, color, on)

def off():
    global strobe_on
    strobe_on = False
    dev.set_color('noColor')

class Pommodoro:
    def __init__(self,work_time=1*60, break_time=1*60):
        self.work_time  = work_time
        self.break_time = break_time
        self.current_time = work_time
        self.on_break   = False
        self.pause = False
        self.set_time_label(work_time)

    def start(self):
        self.current_time = self.work_time
        self._pomm()

    def stop(self):
        self.current_time = 0
        self.on_break = True

    def _pomm(self):
        if self.current_time == 30:
            dev.set_mode('slow')
        elif self.current_time == 15:
            dev.set_mode('fast')
        elif self.current_time == 0:
            dev.set_mode('')

        if self.pause and self.current_time > 0:
            app.after(1000, self._pomm)
        
        elif self.current_time > 0:
            color = 'green' if self.on_break else 'red'
            dev.set_color(color)
            self.current_time -= 1
            self.set_time_label(self.current_time)
            app.after(1000, self._pomm)
        elif not self.on_break:
            dev.set_color('green')
            self.on_break = True
            self.current_time = self.break_time
            app.after(1000, self._pomm)
        else:
            timer.configure(text="00:00")
            dev.rainbow_waterfall()
            dev.set_color('noColor')
            
    def set_time_label(self, time: int):
        minutes = time // 60
        seconds = time % 60
        timer.configure(text=f"{minutes:02}:{seconds:02}")

    def toggle_pause(self):
        self.pause = not self.pause


app = tk.Tk()
app.title('eMetuM')
app.resizable(False, False)
app.configure(background=black)

# Create a label in the window
timer = tk.Label(app, text="Pomodoros")
timer.configure(background=black, foreground='white', font=('Arial', 40), padx=20)
timer.pack(side='left')

# Pommodoro object should be below the timer label so it can access it. 
pom = Pommodoro()

# Buttons 
font = ('Arial', 16, 'bold')
common = {'font': font, 'bd': 0, 'highlightthickness': 0}
btn_frame = tk.Frame(app, bg=black)
btn_frame.pack(side='right', padx=10)
start = tk.Button(btn_frame, text="Start", command=lambda: pom.start(), bg='green', fg='white', **common)
start.pack(side='left', fill='x', expand=True)
pause = tk.Button(btn_frame, text="Pause", command=pom.toggle_pause, bg='orange', fg='white', **common)
pause.pack(side='left')
stop_btn = tk.Button(btn_frame, text="Stop", command=lambda: pom.stop(), bg='red', fg='white', **common)    
stop_btn.pack(side='left', fill='x', expand=True)
bns_btn = tk.Button(btn_frame, text="B", command=lambda: popupmsg(), bg='purple', fg='white', **common)
bns_btn.pack(side='left')

def popupmsg():
    popup = tk.Toplevel(app)
    # Bottom btn row
    bonus_frame = tk.Frame(popup)
    bonus_frame.pack(fill='x')
    dim_btn = tk.Button(bonus_frame, text="Dim", command=lambda: dev.set_mode('dim'), bg='grey', fg='black', **common)
    dim_btn.pack(side='left')
    fast_btn = tk.Button(bonus_frame, text="Fast", command=lambda: dev.set_mode('fast'), **common)
    fast_btn.pack(side='left')
    slow_btn = tk.Button(bonus_frame, text="Slow", command=lambda: dev.set_mode('slow'), **common)
    slow_btn.pack(side='left')
    slow_btn = tk.Button(bonus_frame, text="None", command=lambda: dev.set_mode(''), bg='black', fg='white', **common)
    slow_btn.pack(side='left', fill='x', expand=True)
    rb_btn = tk.Button(bonus_frame, text="Rainbow", command=dev.rainbow_waterfall, bg='magenta', fg='black', **common)
    rb_btn.pack(side='right')
    sb_btn = tk.Button(bonus_frame, text="Strobe", command=lambda: strobe(dev.cur_color), bg='white', fg='black', **common)
    sb_btn.pack(side='right')

    # Color buttons
    color_frame = tk.Frame(popup)
    color_frame.pack(fill='x')
    red_btn = tk.Button(color_frame, text="Red", command=lambda: dev.set_color('red'), bg='red', fg='white', **common)
    red_btn.pack(side='left')
    yellow_btn = tk.Button(color_frame, text="Yellow", command=lambda: dev.set_color('yellow'), bg='yellow', fg='black', **common)
    yellow_btn.pack(side='left')
    green_btn = tk.Button(color_frame, text="Green", command=lambda: dev.set_color('green'), bg='green', fg='white', **common)
    green_btn.pack(side='left')
    cyan_btn = tk.Button(color_frame, text="Cyan", command=lambda: dev.set_color('cyan'), bg='cyan', fg='black', **common)
    cyan_btn.pack(side='left')
    blue_btn = tk.Button(color_frame, text="Blue", command=lambda: dev.set_color('blue'), bg='blue', fg='white', **common)
    blue_btn.pack(side='left')
    purple_btn = tk.Button(color_frame, text="Purple", command=lambda: dev.set_color('purple'), bg='purple', fg='white', **common)
    purple_btn.pack(side='left')
    white_btn = tk.Button(color_frame, text="White", command=lambda: dev.set_color('white'), bg='white', fg='black', **common)
    white_btn.pack(side='left')
    black_btn = tk.Button(color_frame, text="Off", command=lambda: off(), bg='black', fg='white', **common)
    black_btn.pack(side='left')




if __name__ == '__main__':
    app.mainloop()