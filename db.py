import sqlite3, pathlib, os
from datetime import datetime

# Todo
# - Create a categories table
# - create a timer history table

def relative_to_abs_path(rel_path:str) -> str:
    ''' Returns the absolute path of a relative path. '''
    current_dir = pathlib.Path(__file__).parent.resolve() # current directory
    return os.path.join(current_dir, rel_path) 

class Db:
    def __init__(self):


        self.conn = sqlite3.connect(relative_to_abs_path('timer.db'))
        self.conn.row_factory = sqlite3.Row
        self.cursor = self.conn.cursor()
        self._build_db()


    def __del__(self):
        ''' Clean up after ourselves on exit '''
        self.conn.close()

    def _build_db(self):
        ''' Create the timer tables if they don't exist '''
        self._create_table('categories', 'name TEXT, color TEXT, duration INTEGER, rest INTEGER, active INTEGER, UNIQUE(name)')
        self._create_table('timers', 'id INTEGER PRIMARY KEY, start_time TEXT, last_event TEXT, duration INTEGER, rest INTEGER, category TEXT, complete INTEGER')
        self._create_table('events', 'timer_id INTEGER, event TEXT, time TEXT, FOREIGN KEY(timer_id) REFERENCES timers(id)')

        res = self.query("SELECT * FROM categories")
        if not res:
            # Create a default category if there are none
            self.upsert_category('Stopwatch', 'green', 0, 0, True)
            self.upsert_category('Pomodoro', 'red', 25*60, 5*60, True)

    ## SQL basics 
    def query(self, sql:str) -> list:
        self.cursor.execute(sql)
        return self.cursor.fetchall()

    def close(self):
        self.conn.close()

    def _create_table(self, table_name, fields):
        ''' Creates a table if it doesn't exist'''
        sql = "CREATE TABLE IF NOT EXISTS {} ({})".format(table_name, fields)
        self.cursor.execute(sql)
        self.conn.commit()

    ## Categories
    def upsert_category(self, name:str, color:str, duration:int, rest:int, active:bool):
        ''' Updates or inserts a category to the database '''
        # SQLite doesn't have a boolean type, so we convert it to an integer
        active = 1 if active else 0

        # Check for an existing category
        sql = f"""SELECT * FROM categories WHERE name = "{name}" """
        self.cursor.execute(sql)
        if self.cursor.fetchone():
            sql = f"""UPDATE categories SET color = "{color}", duration = {duration}, rest = {rest} active = {active} WHERE name = "{name}" """
        else:
            sql = f"""INSERT INTO categories (name, color, duration, rest, active) VALUES ("{name}", "{color}", {duration}, {rest}, {active})"""
        self.cursor.execute(sql)
        self.conn.commit()

    def get_all_categories(self) -> list:
        ''' Get all categories from the database '''
        sql = "SELECT * FROM categories"
        self.cursor.execute(sql)
        res = [ dict(x) for x in self.cursor.fetchall()]
        return res
    
    def get_active_categories(self) -> list:
        ''' Get all active categories from the database '''
        sql = "SELECT * FROM categories WHERE active = 1"
        self.cursor.execute(sql)
        res = [ dict(x) for x in self.cursor.fetchall()]
        return res
    
    def get_category(self, name:str) -> dict:
        ''' Get a category from the database '''
        sql = f"""SELECT * FROM categories WHERE name = "{name}" """
        self.cursor.execute(sql)
        res = self.cursor.fetchone()
        if res:
            return dict(res)
        else:
            return None

    
    def delete_category(self, name:str) -> None:
        ''' Delete a category from the database '''
        sql = f"""DELETE FROM categories WHERE name = "{name}" """
        self.cursor.execute(sql)
        self.conn.commit()
        

    ## Timers
    def add_timer(self, category:str) -> int:
        ''' Add a timer to the database, duration is in seconds.
            Returns the id of the new timer '''
        start_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        sql = f"""INSERT INTO timers (start_time, category, complete) VALUES ( "{start_time}", "{category}" , 0)"""
        self.cursor.execute(sql)
        self.conn.commit()

        # Return the id of the new timer
        return self.cursor.lastrowid

    def add_event(self, timer_id:int, event:str) -> None:
        ''' Add an event to the database '''
        time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        sql = f"""INSERT INTO events (timer_id, event, time) VALUES ({timer_id}, "{event}", "{time}")"""
        self.cursor.execute(sql)
        self.conn.commit()

    def update_timer(self, timer_id:int, duration:int=None, rest:int=None) -> None:
        ''' Update a timer in the database '''
        if duration is None:
            time = f'rest={rest}'
        else:
            time = f'duration={duration}'

        last_event = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        sql = f"""UPDATE timers SET last_event="{last_event}", {time} WHERE id={timer_id}"""
        self.cursor.execute(sql)
        self.conn.commit()

    def finish_timer(self, timer_id:int) -> None:
        ''' Mark a timer as complete '''
        sql = f"""UPDATE timers SET complete=1 WHERE id={timer_id}"""
        self.cursor.execute(sql)
        self.conn.commit()


