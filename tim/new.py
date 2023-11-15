import argparse
from datetime import datetime, timedelta
from os import path
import sqlite3
import sys

from tim.command import AbstractCommand


class NewCommand(AbstractCommand):
    def __init__(self, args, day_offset):
        super(NewCommand, self).__init__(args, day_offset)

        self.error = False
        self.time = datetime.now()
        parser = argparse.ArgumentParser(
            prog='Tim',
            description='Time tracking helper')
        parser.add_argument('-r', '--retro')
        parser.add_argument('-t', '--time')
        args, argv = parser.parse_known_args(args=self.args)

        options = vars(args)

        if options['time'] is not None:
            self.set_time_by_string(options['time'])
        elif options['retro'] is not None:
            self.time -= timedelta(minutes=int(options['retro']))

        day_offset = timedelta(days=self.day_offset)
        self.time = self.time + day_offset

        self.title = ' '.join(argv)

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
