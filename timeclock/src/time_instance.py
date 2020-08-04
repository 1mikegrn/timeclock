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

    def time_in(self, project=None):
        the_time = datetime.datetime.now()

        self.data = {
            'date': the_time.strftime("%a %b %d %Y"),
            'project': project,
            'time_in': the_time.timestamp(),
            'time_out': None,
            'breaks': [],
            'break_delta': 0.0,
            'work_delta': 'pending...',
        }

        print(f"clocked in at {the_time}")
        print(f"current project: {project}")

        return self

    def time_out(self):
        the_time = datetime.datetime.now()

        self.data['time_out'] = the_time.timestamp()
        self.data['work_delta'] = (
            self.data['time_out'] 
            - self.data['time_in'] 
            - self.data['break_delta']
        )

        print(f"clocked out at {the_time}")

        return self

    def on_break(self,  notes=None):

        the_time = datetime.datetime.now()

        assert self.data != '', ('Must be "in" work so to go "on_break"')

        if len(self.data['breaks']) > 0:
            assert self.data['breaks'][-1]['off_break'] != None, (
                'cannot go "on_break" without first going "off_break"'
            )

        self.data['breaks'].append(
            {
            'notes': notes,
            'on_break': the_time.timestamp(),
            'off_break': None,
            'delta': 'pending...'
            }
        )

        print(f"on break at {the_time}")

        return self

    def off_break(self):

        assert self.data != '', (
            'cannot go "off_break" without first being "in" work and "on_break"'
        )

        assert (
            len(self.data['breaks']) > 0 
            and self.data['breaks'][-1]['off_break'] == None), (
            'cannot go "off_break" without first being "on_break".'
        )

        the_time = datetime.datetime.now()

        entry = self.data['breaks'][-1]
        entry['off_break'] = the_time.timestamp()
        entry['delta'] = the_time.timestamp() - entry['on_break']

        self.data['break_delta'] += entry['delta']

        print(f"off break at {the_time}")

        return self

    def get_status(self, print_msg=True):
        if self.data == '':
            if print_msg == True:
                print('Work status: out')
            else:
                return 'out'

        elif self.data['breaks'] != []:

            if self.data['breaks'][-1]['off_break'] == None:
                if print_msg == True:
                    print(
                        f'''Work status: on_break\nnotes: {
                            self.data['breaks'][-1]['notes']
                        }'''
                    )
                else:
                    return 'on_break'
            else:
                if print_msg == True:
                    print(
                        f'''Work status: in\ncurrent project: {
                                self.data['project']
                        }\nlast break at {
                            datetime.datetime.fromtimestamp(
                                self.data['breaks'][-1]['off_break']
                            ).strftime('%H:%M:%S')
                        }'''
                    )
                else:            
                    return 'in'

        else:
            if print_msg==True:
                print(
                    f'''Work status: in\ncurrent project: {
                        self.data['project']
                    }'''
                )

            else:
                return 'in'

    def from_json(self):
        with open(self.json_path, 'r') as f:
            try:
                data = json.load(f)
            except:
                data = ''
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