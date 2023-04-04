import os
import pathlib

from .looks import Looks

colors = ['red','green','yellow','blue','purple','cyan','white','noColor']

def relative_path(*rel_path:str) -> str:
    ''' Returns the absolute path of a relative path. 
        - rel_path: a list of strings representing the relative path

        Example:
            relative_path('data','timer.db') -> /home/user/timer/data/timer.db
    '''
    current_dir = pathlib.Path(__file__).parent.parent.resolve() # current directory
    if len(rel_path) == 1 and rel_path[0] == '':
        return current_dir
    
    return os.path.join(current_dir, *rel_path) 