from datetime import datetime, timedelta
import getopt
from os import path
import sqlite3
import sys

from tim.command import AbstractCommand


class NewCommand(AbstractCommand):
    def __init__(self, args, day_offset):
        super(NewCommand, self).__init__(args, day_offset)

        self.error = False
        self.time = datetime.now()
        try:
            opts, args = getopt.getopt(self.args, 't:r:', ['retro=', 'time='])
            opt_dict = {x[0]: x[1] for x in opts}
        except getopt.GetoptError:
            sys.exit(2)

        if '-t' in opt_dict:
            self.set_time_by_string(opt_dict['-t'])
        elif '--time' in opt_dict:
            self.set_time_by_string(opt_dict['--time'])
        elif '-r' in opt_dict:
            self.time -= timedelta(minutes=int(opt_dict['-r']))
        elif '--retro' in opt_dict:
            self.time -= timedelta(minutes=int(opt_dict['--retro']))

        self.title = ' '.join(args)

    def set_time_by_string(self, time_string) -> None:
        try:
            self.time = datetime.strptime(
                self.time.strftime('%d-%m-%Y') + ' ' +
                time_string, '%d-%m-%Y %H:%M')
        except ValueError:
            self.error = 'Incorrect time pattern, please use the pattern ' \
                         'HH:MM (eg. 13:45).'

    def run(self) -> None:
        if self.error is not False:
            print(self.error)
            exit(1)

        timestamp = self.time.timestamp()

        tim_dir = path.dirname(path.dirname(path.realpath(__file__)))
        db = path.join(tim_dir, 'db', 'tim.sqlite')
        conn = sqlite3.connect(db)
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO timestamps (timestamp, title) VALUES (?, ?);',
            [timestamp, self.title])
        conn.commit()
