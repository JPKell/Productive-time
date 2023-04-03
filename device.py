import pathlib, os
import subprocess
import time

def relative_to_abs_path(rel_path:str) -> str:
    ''' Returns the absolute path of a relative path. '''
    current_dir = pathlib.Path(__file__).parent.resolve() # current directory
    return os.path.join(current_dir, rel_path) 

class Emetum:
    colors = {
        'red':     1,
        'green':   2,
        'yellow':  3,
        'blue':    4,
        'purple':  5,
        'cyan':    6,
        'white':   7,
        'noColor': 8,
        }

    # Can take one of the following mods
    modes = {
        'dim': 10,
        'fast': 20,
        'slow': 30,
    }

    def __init__(self):
        self.mode = ''
        self.usb_dev = str(subprocess.check_output(relative_to_abs_path("find_dev_file.sh")), 'utf-8').strip()
        self.sh_path = relative_to_abs_path("emetum.sh")
        self.cur_color = 'noColor'
        self._buf_color = 'noColor'
        self.strobe_active = False  
        self.loop = None

    def __del__(self):
        self.set_color('noColor')

    def register_loop(self, loop):
        self.loop = loop

    def set_mode(self, mode, coro:object=None) -> None:
        ''' coro is passed to strobe only'''
        self.mode = mode
        if mode == 'strobe':
            self.strobe(coro, self.cur_color)
        else:
            if self.strobe_active:
                self.strobe_active = False
            self.set_color(self.cur_color)

    def set_color(self, color, mode='', retain_old_color=False) -> None:
        ''' Can take an int or a string
            `['red','yellow','green','cyan','blue','purple','white', 'noColor']`
        '''
        if color not in self.colors.keys():
            print('Invalid color')
            return
        if not retain_old_color:
            self.cur_color = color 
        # If mod is not in mods, set it to class mode
        mode = self.modes.get(mode, self.modes.get(self.mode,0))
        color = f'\\x{self.colors[color] + mode :02}'
        subprocess.run([self.sh_path, color, self.usb_dev])

    def rainbow_waterfall(self):
        for c in ['red','yellow','green','cyan','blue','purple']:
            self.set_color(c)
            time.sleep(0.05)

    def strobe(self):
        ''' Strobes the light. '''
        if self.strobe_active:
            self.strobe_active = False
        else:
            self.strobe_active = True
            self._strobe()     

    def _strobe(self, on=True) -> None:
        ''' Underlying function for strobe. '''
        if self.strobe_active:
            if not on:
                self.set_color('noColor', retain_old_color=True)
            else:
                self.set_color(self.cur_color)
            on = not on
            self.loop(30, self._strobe, on)
        else:
            # Restore the light to on after strobe
            self.set_color(self.cur_color)