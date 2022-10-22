from datetime import datetime
from os import path
import re
import sqlite3
import sys
from tabulate import tabulate
import time

from tim.command import AbstractCommand


class GroupCommand(AbstractCommand):
    """Group tracked timestamps under the same title."""

    def run(self) -> None:
        tim_dir = path.dirname(path.dirname(path.realpath(__file__)))
        db = path.join(tim_dir, 'db', 'tim.sqlite')
        conn = sqlite3.connect(db)
        cursor = conn.cursor()

        print('\033[1m\n\033[33mToday,',
              time.strftime('%d-%m-%Y'),
              '\033[0m\n')

        timestamps = cursor.execute(
            "SELECT timestamp, title FROM timestamps "
            "WHERE timestamp >= strftime('%s', 'now', 'start of day') "
            "ORDER BY timestamp ASC;").fetchall()
        timestamps_print = [
            (datetime.fromtimestamp(x[0]).strftime('%H:%M'), x[1])
            for x in timestamps]
        print(tabulate(timestamps_print, headers=['Time', 'Title'],
              showindex=True))

        timestamps = [
            (x[0], datetime.fromtimestamp(x[0]).strftime('%H:%M'), x[1])
            for x in timestamps
        ]

        while True:
            action = input('\nEnter the indeces to group (or q to quit): ')
            action = action.lower()

            if action == 'q':
                break

            if action is not False:
                if re.fullmatch(r'([0-9]+, *)*[0-9]+', action) is None:
                    print('The input is incorrect. Please supply the indeces '
                          'of the timestamps you want to group seperated by a '
                          'comma. Or q to quit.')
                else:
                    indeces = [int(x.strip()) for x in action.split(',')]
                    group_stamps = [timestamps[x] for x in indeces]

                    print('\n')
                    print(tabulate([[x[1], x[2]] for x in group_stamps],
                          headers=['Time', 'Title']))

                    title = input('\nEnter a new title for these stamps: ')
                    print(title)

        sys.exit(0)
