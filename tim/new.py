from datetime import datetime
import getopt
from os import path
import sqlite3
import sys

from tim.command import AbstractCommand


class NewCommand(AbstractCommand):
    def __init__(self, args, day_offset):
        super(NewCommand, self).__init__(args, day_offset)

        self.minute_delta = 0
        try:
            opts, args = getopt.getopt(self.args, 'r:', ['retro='])
            opt_dict = {x[0]: x[1] for x in opts}
        except getopt.GetoptError:
            sys.exit(2)

        if '-r' in opt_dict:
            self.minute_delta = int(opt_dict['-r'])
        elif '--retro' in opt_dict:
            self.minute_delta = int(opt_dict['--retro'])

        self.title = ' '.join(args)

    def run(self) -> None:
        timestamp = datetime.timestamp(datetime.now())
        timestamp = int(timestamp - self.minute_delta * 60)

        tim_dir = path.dirname(path.dirname(path.realpath(__file__)))
        db = path.join(tim_dir, 'db', 'tim.sqlite')
        conn = sqlite3.connect(db)
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO timestamps (timestamp, title) VALUES (?, ?);',
            [timestamp, self.title])
        conn.commit()
