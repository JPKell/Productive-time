from db import Db
from view import App
from device import Emetum
import settings

class Controller:

    def __init__(self):
        self.db  = Db()
        self.lights = Emetum()

        self._light_color = 'noColor'
        self._light_mode = ''
       
        self.app = App(self)

        # Register the event loop with lights so it can have timing
        self.lights.register_loop(self.app.after)

        self.app.protocol('WM_DELETE_WINDOW', self.on_close)
        self.app.mainloop()

    @property
    def light_color(self) -> str:
        return self._light_color
    
    @light_color.setter
    def light_color(self, color:str):
        if color not in self.lights.colors:
            raise ValueError(f'Invalid color: {color}')
        self._light_color = color
        self.lights.set_color(color)

    @property
    def light_mode(self) -> str:
        return self._light_mode
    
    @light_mode.setter
    def light_mode(self, mode:str):
        valid_modes  = list(self.lights.modes.keys()) + ['', 'strobe']
        if mode not in valid_modes:
            raise ValueError(f'Invalid mode: {mode}')
        
        if mode == 'strobe':
            self._light_mode = mode
            self.lights.strobe()
        elif mode == self._light_mode:
            # Toggle off if the mode is selected again
            self._light_mode = ''
            self.lights.set_mode('')
        else:
            self._light_mode = mode
            self.lights.set_mode(mode)

    def on_close(self):
        self.lights.set_color('noColor')
        for timer in self.app.timers:
            timer.delete_timer()
        self.app.destroy()

    def upsert_category(self, form:dict):
        self.db.upsert_category(**form)

    def get_category_list(self):
        return self.db.get_all_categories()
    
    def get_category(self, name:str):
        return self.db.get_category(name)

    def delete_category(self, name:str):
        self.db.delete_category(name)

    def insert_timer(self, category:str) -> int:
        id = self.db.add_timer(category)
        return id
    
    def update_timer(self, id:int, duration:int=None, rest:int=None):
        if duration != None and rest != None:
            self.db.update_timer(id, duration=duration)
            self.db.update_timer(id, rest=rest)
        elif duration != None:
            self.db.update_timer(id, duration=duration)
        elif rest != None:
            self.db.update_timer(id, rest=rest)

    def finish_timer(self, id:int):
        self.db.finish_timer(id)

    def add_event(self, timer_id:int, event:str):
        self.db.add_event(timer_id, event)

if __name__ == '__main__':
    Controller()