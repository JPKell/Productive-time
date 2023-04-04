import pathlib, os
import subprocess
import time

from settings import relative_path

class MuteMe:
    ''' Linux only. The easiest way to interact with the MuteMe device is
        echoing the color to the device file. No plans to support Windows
        at this time.

        The MuteMe device is good while you are in a meeting, this makes
        use of the MuteMe device to alert the user of their timer status.
        
        If the MuteMe software has been installed already, this will work
        out of the box. Otherwise, you will need to either install the
        software or run the scripts/create_rules.sh script manually. This
        will set permissions on the device file so that the app can write 
        to it.    
    '''

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

    # Can take one of the following modes
    modes = {
        'dim': 10,
        'fast': 20,
        'slow': 30,
    }

    def __init__(self):
        # Do not initialize if not on Linux
        if os.name != 'posix':
            raise OSError('MuteMe integration available on Linux only')
        
        self.usb_dev = str(subprocess.check_output(relative_path("scripts", "find_dev_file.sh")), 'utf-8').strip()
        if self.usb_dev == '':
            raise FileNotFoundError('MuteMe device not found')

        self.echo_path = relative_path("scripts", "muteme_echo.sh")
        
        # Various variables
        self._on = True
        self.mode = ''
        self.cur_color = 'noColor'
        self._buf_color = 'noColor'
        self.strobe_active = False  
        self.loop = None

    def __del__(self) -> None:
        ''' Turn off the light on exit'''
        if hasattr(self, 'usb_dev') and self.usb_dev != '':
            self.set_color('noColor')

    @property
    def on(self) -> bool:
        return self._on
    
    @on.setter
    def on(self, on:bool) -> None:
        if not on:
            self.set_color('noColor', retain_old_color=True)
            self._on = on
        else:
            self._on = on
            self.set_color(self.cur_color)

    def register_loop(self, loop:object) -> None:
        ''' Register the asyncio loop so that we can run coroutines '''
        self.loop = loop

    def set_mode(self, mode) -> None:
        ''' Sets the mode of the light to one of the following:
            `['dim','fast','slow', 'strobe']`
        '''
        self.mode = mode
        if mode == 'strobe':
            self.set_color(self.cur_color)
            self.toggle_strobe()
        else:
            if self.strobe_active:
                self.strobe_active = False
            self.set_color(self.cur_color)

    def set_color(self, color, mode='', retain_old_color=False) -> None:
        ''' Can take an int or a string
            `['red','yellow','green','cyan','blue','purple','white', 'noColor']`
            - `retain_old_color` will keep the current color as the local variable
              useful for strobe and other times you want to turn the light off 
              and restore the previous color on a later call.
        '''
        if color not in self.colors.keys():
            raise ValueError(f'Invalid color: {color}')

        if not retain_old_color:
            self.cur_color = color 

        if not self._on:
            return

        # If mode is not in modes, set it to class mode, fallback to no mode
        mode = self.modes.get(mode, self.modes.get(self.mode,0))
        
        # Add the mode to the color and convert to hex string
        color = f'\\x{self.colors[color] + mode :02}'
        res = subprocess.run([self.echo_path, color, self.usb_dev], capture_output=True)
        
        if res.returncode != 0:
            self.usb_dev = ''
            raise OSError(f'Error setting color: {res.stderr}')

    def toggle_strobe(self) -> None:
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