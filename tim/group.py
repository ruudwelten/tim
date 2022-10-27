from datetime import datetime
from os import path
import re
import sqlite3
from tabulate import tabulate

from tim.command import AbstractCommand


class GroupCommand(AbstractCommand):
    """Group tracked timestamps under the same title."""

    def run(self) -> None:
        tim_dir = path.dirname(path.dirname(path.realpath(__file__)))
        db = path.join(tim_dir, 'db', 'tim.sqlite')
        conn = sqlite3.connect(db)
        cursor = conn.cursor()

        while True:
            print(f'\033[1m\n\033[33m{self.printed_day}\033[0m\n')

            timestamps = cursor.execute(
                'SELECT timestamp, title, tally FROM timestamps '
                f'WHERE timestamp >= {self.start} AND timestamp < {self.end} '
                'ORDER BY timestamp ASC;').fetchall()
            timestamps_print = [
                (datetime.fromtimestamp(x[0]).strftime('%H:%M'),
                 x[1],
                 'Yes' if x[2] == 1 else 'No')
                for x in timestamps]
            print(tabulate(timestamps_print, headers=['Time', 'Title', 'Tallied'],
                showindex=True))

            timestamps = [
                (x[0],
                 datetime.fromtimestamp(x[0]).strftime('%H:%M'),
                 x[1],
                 x[2])
                for x in timestamps
            ]

            action = ''
            while action == '' or action == '?':
                if action == '?':
                    print('\n'
                          '\033[36mOptions:\033[0m\n'
                          '  \033[1m[g]roup\033[0m  Group timestamps under the same title\n'
                          '  \033[1m[t]oggle\033[0m Toggle the tally status of the timestamp\n'
                          '  \033[1m[q]uit\033[0m   Quit Tim\n'
                          '  \033[1m[?]\033[0m      Show these instructions')

                action = input('\n\033[33mWhat do you want to do? [g, t, q, ?]: \033[0m')
                action = action.lower()

            if action == 'q':
                break

            if action == 'g':
                action = input('\n\033[33mEnter the indeces to group (or c to '
                               'cancel, q to quit): \033[0m')
                action = action.lower()

                if action == 'c':
                    continue
                if action == 'q':
                    break

                if re.fullmatch(r'([0-9]+, *)*[0-9]+', action) is None:
                    print('The input is incorrect. Please supply the indeces '
                          'of the timestamps you want to group seperated by a '
                          'comma.')
                else:
                    indeces = [int(x.strip()) for x in action.split(',')]
                    group_stamps = [timestamps[x] for x in indeces]

                    print('\n')
                    print(tabulate([[x[1], x[2]] for x in group_stamps],
                          headers=['Time', 'Title']))

                    title = input('\n\033[33mEnter a new title for these '
                                  'stamps: \033[0m')

                    for stamp in group_stamps:
                        query = f'''UPDATE timestamps SET title = \'{title}\'
                                    WHERE timestamp = {stamp[0]};'''
                        cursor.execute(query)
                    conn.commit()
            elif action == 't':
                action = input('\n\033[33mEnter the indeces to toggle if they '
                               'are tallied (or c to cancel, q to quit): '
                               '\033[0m')
                action = action.lower()

                if action == 'c':
                    continue
                if action == 'q':
                    break

                if re.fullmatch(r'([0-9]+, *)*[0-9]+', action) is None:
                    print('The input is incorrect. Please supply the indeces '
                          'of the timestamps for which you want to toggle if '
                          'they are tallied.')
                else:
                    indeces = [int(x.strip()) for x in action.split(',')]
                    toggle_stamps = [timestamps[x] for x in indeces]

                    for stamp in toggle_stamps:
                        new_tally = 0 if stamp[3] == 1 else 1
                        query = f'''UPDATE timestamps SET tally = {new_tally}
                                    WHERE timestamp = {stamp[0]};'''
                        cursor.execute(query)
                    conn.commit()
