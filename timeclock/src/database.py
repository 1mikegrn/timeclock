import time
import datetime
import sqlite3
import pandas as pd

from os import path
from random import randint

class DataBaseManager:
    def __init__(self, path):
        self.conn = sqlite3.connect(path)
        self.sql = self.conn.cursor()

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.sql.close()
        self.conn.close()

    def execute(self, *args, r=False):
        res = self.sql.execute(*args)
        if r == False: 
            return self
        else: 
            return res

    def commit(self):
        self.conn.commit()


class DataBase:
    def __init__(self):
        self.path = path.join(
            path.dirname(path.abspath(__file__)), 
            'database', 
            'data.db'
        )

    def execute_and_commit(self, *args):
        with DataBaseManager(self.path) as sql:
            sql.execute(*args).commit()

    def create_db(self):
        self.execute_and_commit(
            """
            CREATE TABLE IF NOT EXISTS timeclock (
                id INTEGER PRIMARY KEY,
                date TEXT,
                task TEXT,
                time_in REAL,
                time_out REAL,
                break_log TEXT,
                break_delta REAL,
                work_delta REAL
            )
            """
        )
        return self

    def commit_time_instance(self, TimeInstance, clear=True):

        if TimeInstance.get_status(print_msg=False) == 'on_break':
            TimeInstance = TimeInstance.off_break()

        break_id = self._break_log()

        columns = [x for x in TimeInstance.data.keys() if x != 'breaks']

        self.execute_and_commit(
            f"""
                INSERT INTO timeclock(
                    {', '.join(columns)}, break_log
                ) VALUES(
                    {', '.join(['?' for _ in range(len(columns) + 1)])}
                )
            """, 
            [TimeInstance.data[x] for x in columns] + [break_id]
        )

        for break_instance in TimeInstance.data['breaks']:
            break_columns = [x for x in break_instance.keys()]

            self.execute_and_commit(
                f"""
                INSERT INTO {break_id}(
                    {', '.join(break_columns)}
                ) VALUES (
                    {', '.join(['?' for _ in range(len(break_columns))])}
                )
                """, [break_instance[x] for x in break_columns]
            )

        if clear == True:
            TimeInstance._clear_json()

    def get_database(self, output_format=None):

        with DataBaseManager(self.path) as sql:
            table = pd.read_sql_query(
                "SELECT * FROM timeclock", 
                sql.conn,
                )

        if output_format in ['epoch', 'e']:
            return table
        else:
            return self._convert(
                table, 
                ['time_in', 'time_out'], 
                ['break_delta', 'work_delta']
            )

    def get_break_log(self, break_id, output_format):
        with DataBaseManager(self.path) as sql:
            table = pd.read_sql_query(
                f"SELECT * FROM {break_id}", 
                sql.conn,
            )
        if output_format in ['epoch']:
            return table
        else:
            return self._convert(
                table, 
                ['on_break', 'off_break'], 
                ['delta']
            )

    def _convert(self, table, _convert_times, _covert_deltas):

        for col in _convert_times:
            table[col] = table[col].apply(
                lambda x: datetime.datetime.fromtimestamp(
                    x
                ).strftime('%H:%M:%S')
            )

        for col in _covert_deltas:
            table[col] = table[col].apply(
                lambda x: datetime.timedelta(seconds=x)
            )

        return table

    def _break_log(self):

        table_id = self._get_id(self._get_table_names())

        self.execute_and_commit(
            f"""
            CREATE TABLE IF NOT EXISTS {table_id} (
                notes TEXT,
                on_break REAL,
                off_break REAL,
                delta REAL
            )
            """
        )

        return table_id

    def _get_id(self, names, count=0):

        name = ''.join(
            [chr(randint(65, 90)) for _ in range(7)]
        )

        if name not in names:
            return name
        elif count < 1000:
            return self._get_id(names, count+1)
        else:
            raise RuntimeError(
        'FAILED TO GENERATE UNIQUE ID AFTER 1000 ATTEMPTS'
        )

    def _get_table_names(self):
        with DataBaseManager(self.path) as sql:
            names = [x[0] for x in sql.execute(
                "SELECT name FROM sqlite_master WHERE type='table'",
                r=True
            )]

        return names

    def _drop_db(self, name):
        self.execute_and_commit(
            f"""
            DROP TABLE {name}
            """
        )

    def _reset_db(self):
        names = self._get_table_names()
        for name in names:
            self._drop_db(name)
        self.create_db()


if __name__ == "__main__":
    db = DataBase()

    db.create_db()
    db._break_log()
    
    db._drop_db('timeclock')


