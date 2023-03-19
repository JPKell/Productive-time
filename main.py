import subprocess
import time
import binascii
# Yes this is linux only, it's a personal project.
path = '/dev/hidraw1'

# These values are take from the source code of the original software.
# colors = {
#     'red':     b"\x01\x20\x06\x05\x04\x03\x02\x01",
#     'green':   b"\x02\x20\x06\x05\x04\x03\x02\x01",
#     'blue':    b"\x03\x20\x06\x05\x04\x03\x02\x01",
#     'yellow':  b"\x04\x20\x06\x05\x04\x03\x02\x01",
#     'cyan':    b"\x05\x20\x06\x05\x04\x03\x02\x01",
#     'purple':  b"\x06\x20\x06\x05\x04\x03\x02\x01",
#     'white':   b"\x07\x20\x06\x05\x04\x03\x02\x01",
#     'noColor': b"\x00\x20\x06\x05\x04\x03\x02\x01",
#     }
colors = {
    'red':     b'01000000',
    'green':   '0x02',
    'blue':    '0x03',
    'yellow':  '04',
    'cyan':    '55',
    'purple':  '06',
    'white':   '07',
    'noColor': '00',
    }

def set_color(file, color) -> None:
    ''' Can take an int or a string
        `['red','yellow','green','cyan','blue','purple','white']`
    '''
    file.seek(0)
    file.write(colors[color])
 
    return
    if isinstance(color, str):
        subprocess.run([f"""echo {colors[color]} > {path}"""], shell=True)
    if isinstance(color, int):
        subprocess.run([f'echo {color} > {path}'], shell=True)


def rainbow_waterfall(f):
    for c in ['red','yellow','green','cyan','blue','purple']:
        set_color(f,c)
        time.sleep(0.25)

def strobe(f):
    while True:
        set_color(f,'white')
        time.sleep(0.02)
        set_color(f,'noColor')
        time.sleep(0.03)

def pommodoro(f):
    for i in range(4):
        set_color(f,'red')
        time.sleep(25*60)
        set_color(f,'green')
        time.sleep(5*60)

def select_color(f):
    while True:
        color = input('Enter a color: ')
        if color in colors.keys():
            set_color(f,color)
        else:
            print('Invalid color')

import os
if __name__ == '__main__':
        
    # try:
        with open(path, 'bw') as f:

            
            while True:

                # rainbow_waterfall(f)
                # strobe()
                # pommodoro()
                select_color(f)
    # except KeyboardInterrupt:
    #     print("exiting...")
    # except Exception as e:
    #     print(e)
    # finally:
    #     set_color(None,'noColor',)