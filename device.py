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
    mods = {
        'dim': 10,
        'fast': 20,
        'slow': 30,
    }

    def __init__(self):
        self.mode = ''
        self.usb_dev = str(subprocess.check_output(relative_to_abs_path("find_dev_file.sh")), 'utf-8').strip()
        self.sh_path = relative_to_abs_path("emetum.sh")
        self.cur_color = 'noColor'

    def __del__(self):
        self.set_color('noColor')

    def set_mode(self, mode):
        self.mode = mode
        self.set_color(self.cur_color)

    def set_color(self, color, mod='', retain_old_color=False) -> None:
        ''' Can take an int or a string
            `['red','yellow','green','cyan','blue','purple','white', 'noColor']`
        '''
        if color not in self.colors.keys():
            print('Invalid color')
            return
        if not retain_old_color:
            self.cur_color = color 
        # If mod is not in mods, set it to class mode
        mod = self.mods.get(mod, self.mods.get(self.mode,0))
        color = f'\\x{self.colors[color] + mod :02}'
        subprocess.run([self.sh_path, color, self.usb_dev])

    def rainbow_waterfall(self):
        for c in ['red','yellow','green','cyan','blue','purple']:
            self.set_color(c)
            time.sleep(0.05)

    def select_color(self):
        while True:
            color = input('Enter a color: ')
            color = color.lower().split(' ')
            # Incase no mod was entered, add an empty string to avoid index error
            color.append('')
            if color[0] in self.colors.keys():
                self.set_color(color[0], color[1], retain_old_color=True)
            else:
                print('Invalid color')

