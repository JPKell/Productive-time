from   datetime import datetime
import sqlite3
# Local imports
from   settings import relative_path


class Db:
    ''' Stores the categories and timer records in an SQLite database '''
    def __init__(self):
        self.conn = sqlite3.connect(relative_path('data','timer.db'))
        # Return rows as dictionaries
        self.conn.row_factory = sqlite3.Row
        self.cursor = self.conn.cursor()
        self._build_db()

    def __del__(self):
        ''' Clean up after ourselves on exit '''
        self.conn.close()

    def _build_db(self) -> None:
        ''' Create the timer tables if they don't exist '''
        # Build the columns for each table
        categories = '''
            id INTEGER PRIMARY KEY, parent_id INTEGER, sort INTEGER, name TEXT, color TEXT, duration INTEGER, active INTEGER
        '''
        timers = '''
            id INTEGER PRIMARY KEY, category_id INTEGER, start_time TEXT, last_event TEXT, duration INTEGER, complete INTEGER
        '''
        events = '''
            timer_id INTEGER, event TEXT, time TEXT, FOREIGN KEY(timer_id) REFERENCES timers(id)
        '''

        # Create the tables if they don't exist
        self._create_table('categories', categories)
        self._create_table('timers', timers)
        self._create_table('events', events)

        # Check for categories and create defaults if there are none
        res = self.query("SELECT * FROM categories")
        if not res:
            # Create a default category if there are none
            self.upsert_category('Stopwatch', 'purple', 0, True)
            self.upsert_category('Pomodoro', 'red', 25*60, True)
            self.upsert_category('Rest', 'green', 5*60, True, parent_id=2, sort=1)

    ## SQL basics 
    def query(self, sql:str) -> list:
        self.cursor.execute(sql)
        return self.cursor.fetchall()

    def close(self):
        self.conn.close()

    def _create_table(self, table_name, fields):
        ''' Creates a table if it doesn't exist'''
        sql = f"CREATE TABLE IF NOT EXISTS {table_name} ({fields})"
        self.cursor.execute(sql)
        self.conn.commit()

    ## Categories
    def upsert_category(self, name:str, color:str, duration:int, active:bool=True, id:int=None, parent_id:int=None, sort:int=None):
        ''' Updates or inserts a category to the database '''
        # SQLite doesn't have a boolean type, so we convert it to an integer
        active = 1 if active else 0
        if parent_id == None:
            parent_id = "NULL"

        if id != None:
            if sort != None:
                sort = f'sort={sort},'
            sql = f"""UPDATE categories SET name = "{name}", color = "{color}", duration = {duration}, {sort} active = {active} WHERE id = "{id}" """
        else:
            if sort == None:
                sort = 0
            sql = f"""INSERT INTO categories (parent_id, sort, name, color, duration, active) VALUES ({parent_id}, {sort},"{name}", "{color}", {duration},  {active})"""
        self.cursor.execute(sql)
        self.conn.commit()

        return self.cursor.lastrowid

    def get_all_categories(self) -> list:
        ''' Get all categories from the database '''
        sql = "SELECT * FROM categories"
        self.cursor.execute(sql)
        res = [ dict(x) for x in self.cursor.fetchall()]
        return res
    
    def get_root_categories(self) -> list:
        ''' Get all categories from the database '''
        sql = "SELECT * FROM categories WHERE parent_id IS NULL"
        self.cursor.execute(sql)
        res = [ dict(x) for x in self.cursor.fetchall()]
        return res
    
    def get_active_categories(self) -> list:
        ''' Get all active categories from the database '''
        sql = 'SELECT * FROM categories WHERE active = 1 '
        self.cursor.execute(sql)
        res = [ dict(x) for x in self.cursor.fetchall()]
        return res
    
    def get_category(self, name:str) -> dict:
        ''' Get a category from the database '''
        sql = f'SELECT * FROM categories WHERE name = "{name}" '
        self.cursor.execute(sql)
        res = self.cursor.fetchone()
        if res:
            return dict(res)
        else:
            return None
    
    def get_parent_category(self, id:int) -> dict:
        ''' Get a category from the database '''
        sql = f'SELECT * FROM categories WHERE id = "{id}" '
        self.cursor.execute(sql)
        res = self.cursor.fetchone()
        if res:
            return dict(res)
        else:
            return None

    def deactivate_category(self, id:int) -> None:
        ''' Delete a category from the database '''
        sql = f'UPDATE categories SET active = 0 WHERE id = {id} '
        self.cursor.execute(sql)
        self.conn.commit()

    def delete_category(self, id:int) -> None:
        ''' Delete a category and children from the database '''
        sql = f'DELETE FROM categories WHERE id = {id} OR parent_id = {id} '
        self.cursor.execute(sql)
        self.conn.commit()
        
    def get_chained_timers(self, id:int) -> list:
        ''' Get all categories from the database '''
        sql = f"SELECT * FROM categories WHERE parent_id = {id} ORDER BY sort"
        self.cursor.execute(sql)
        res = [ dict(x) for x in self.cursor.fetchall()]
        return res

    ## Timers
    def add_timer(self, category_id:int) -> int:
        ''' Add a timer to the database, duration is in seconds.
            Returns the id of the new timer '''
        start_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        sql = f'INSERT INTO timers (start_time, category_id, complete) VALUES ( "{start_time}", "{category_id}" , 0)'
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

    def get_timer_report(self, period:str) -> dict:
        ''' Get a dict to generate a report of all timers in a period '''
        if period == 'all':
            sql = f"""SELECT * FROM timers"""
        else:
            sql = f"""SELECT t.* FROM timers t JOIN categories c ON t.category_id = c.id WHERE start_time > date('now', '-{period} days')"""
        self.cursor.execute(sql)
        # Convert the results to a list of dicts
        res = [ dict(x) for x in self.cursor.fetchall()]

        # Dictionary to hold the report has each category as a key and a list of timers as the value
        report = {}
        categories = self.get_all_categories()
        for cat in categories:
            report[cat['name']] = [ d for d in res if d['category'] == cat['name'] ]

        return report
