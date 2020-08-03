import sys
import time
from os import path

# sys.path.insert(0, path.split(path.abspath(path.dirname(__file__)))[0])
import timeclock

def main():
    cmd, options = timeclock.src.cmd_reader.reader()

    inst = timeclock.src.time_instance.TimeInstance
    db = timeclock.src.database.DataBase

    if cmd == 'status':
        inst().from_json().get_status()

    elif cmd in ['in', 'n']:
        inst().time_in().to_json()

    elif cmd in ['out', 'o']:
        db().commit_time_instance(
            inst().from_json().time_out()
        )

    elif cmd in ['on_break', '+b']:
        message = options['-m'] if '-m' in options else None
        inst().from_json().on_break(message).to_json()

    elif cmd in ['off_break', '-b']:
        inst().from_json().off_break().to_json()

    elif cmd in ['get_db', 'db']:
        output_format = options['-f'] if '-f' in options else None
        print(db().get_database(output_format))

    elif cmd in ['get_logs', 'log', 'lg']:
        assert ('-id' in options), ('get_logs requires format -id <ID>')

        output_format = options['-f'] if '-f' in options else None
        print(db().get_break_log(options['-id'], output_format))

    elif cmd == 'RESET':
        confirm = input(
            'Please confirm RESET; this action can not be undone. [Y]: '
        )
        if confirm == 'Y':
            db()._reset_db()
            inst()._clear_json()
        else:
            print('Operation aborted')

def _test():
    db = timeclock.src.database.DataBase
    inst = timeclock.src.time_instance.TimeInstance

    inst().time_in().to_json()

    inst().from_json().on_break('meeting').to_json()
    time.sleep(0.5)
    inst().from_json().off_break().to_json()

    inst().from_json().on_break('lunch').to_json()
    time.sleep(0.25)
    inst().from_json().off_break().to_json()

    inst().from_json().on_break('walk dog').to_json()
    time.sleep(0.5)
    inst().from_json().off_break().to_json()

    out = inst().from_json().time_out()

    db().create_db()
    db().commit_time_instance(out, clear=False)

    table = db().get_database()

    logs = db().get_break_log(table['break_log'].iloc[-1], None)

    print('\n')
    print(table)
    print('\n')
    print(logs)

    db()._reset_db()
    inst()._clear_json()

# if __name__ == "__main__":
#     _test()