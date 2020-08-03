import time
import datetime
import json

from os import path

here = path.dirname(path.abspath(__file__))

class TimeInstance:
    def __init__(self):
        self.json_path = path.join(
            path.dirname(path.abspath(__file__)), 
            'database', 
            'persist.json'
        )

    def time_in(self):
        self.data = {
            'date': datetime.datetime.today().strftime("%a %b %d %Y"),
            'time_in': time.time(),
            'time_out': None,
            'breaks': [],
            'break_delta': 0.0
        }
        return self

    def time_out(self):
        self.data['time_out'] = time.time()
        return self

    def on_break(self,  notes=None):

        if len(self.data['breaks']) > 0:
            assert self.data['breaks'][-1]['off_break'] != None, (
                'can not start break without first ending previous break'
            )

        self.data['breaks'].append(
            {
            'notes': notes,
            'on_break': time.time(),
            'off_break': None,
            'delta': 'pending...'
            }
        )
        return self

    def off_break(self):
        assert self.data['breaks'][-1]['off_break'] == None, (
            'can not end break without first initializing break'
        )

        off_time = time.time()

        entry = self.data['breaks'][-1]
        entry['off_break'] = off_time
        entry['delta'] = off_time - entry['on_break']

        self.data['break_delta'] += entry['delta']
        return self

    def from_json(self):
        with open(self.json_path, 'r') as f:
            data = json.load(f)
        self.data = data
        return self

    def to_json(self):
        with open(self.json_path, 'w') as f:
            json.dump(self.data, f, indent=2)
        return self

    def _clear_json(self):
        open(self.json_path, 'w').close()

if __name__ == "__main__":
    import time

    TimeInstance().time_in().to_json()

    time.sleep(0.5)
    TimeInstance().from_json().on_break().to_json()
    time.sleep(0.5)
    TimeInstance().from_json().off_break().to_json()
    time.sleep(0.5)
    TimeInstance().from_json().on_break().to_json()
    time.sleep(0.5)
    TimeInstance().from_json().off_break().to_json()

    print(TimeInstance().from_json().data)