import sys
import time
from os import path

# sys.path.insert(0, path.split(path.abspath(path.dirname(__file__)))[0])
import timeclock

def main():
    cmd, options = timeclock.src.cmd_reader.reader()

    inst = timeclock.src.time_instance.TimeInstance
    db = timeclock.src.database.DataBase

    if cmd == 'in':
        inst().time_in().to_json()

    elif cmd == 'out':
        db().commit_time_instance(
            inst().from_json().time_out()
        )

    elif cmd == 'on_break':
        inst().from_json().on_break(options['-m']).to_json()

    elif cmd == 'off_break':
        inst().from_json().off_break().to_json()

    elif cmd == 'get_db':
        print(db().get_database())

    elif cmd == 'get_logs':
        print(db().get_break_log(options['-id']))


# def _test():
#     db = timeclock.src.database.DataBase
#     inst = timeclock.src.time_instance.TimeInstance

#     inst().time_in().to_json()

#     inst().from_json().on_break('meeting').to_json()
#     time.sleep(0.5)
#     inst().from_json().off_break().to_json()

#     inst().from_json().on_break('lunch').to_json()
#     time.sleep(0.25)
#     inst().from_json().off_break().to_json()

#     inst().from_json().on_break('walk dog').to_json()
#     time.sleep(0.5)
#     inst().from_json().off_break().to_json()

#     out = inst().from_json().time_out()

#     db().create_db()
#     db().commit_time_instance(out, clear=False)

#     table = db().get_database()

#     logs = db().get_break_log(table['break_log'].iloc[-1])

#     print(table)
#     print('\n')
#     print(logs)

# if __name__ == "__main__":
#     _test()