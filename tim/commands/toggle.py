import re
import sqlite3
from datetime import datetime
from os import path

from tabulate import tabulate

from tim import TIM_DIR
from tim.commands import AbstractCommand
from tim.commands.registry import CommandRegistry


@CommandRegistry.register('toggle')
class ToggleCommand(AbstractCommand):
    """Toggle the tally status of a timestamp"""

    def run(self) -> None:
        db = path.join(TIM_DIR, 'db', 'tim.sqlite')
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
            print(tabulate(timestamps_print,
                           headers=['Time', 'Title', 'Tallied'],
                           showindex=True))

            timestamps = [
                (x[0],
                 datetime.fromtimestamp(x[0]).strftime('%H:%M'),
                 x[1],
                 x[2])
                for x in timestamps
            ]

            action = input('\n\033[33mEnter the indeces to toggle if they are '
                           'tallied (or q to quit): \033[0m')
            action = action.lower()

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

                toggle_stamps_where = " OR ".join(f"timestamp = {str(x[0])}"
                                                  for x in toggle_stamps)
                timestamps = cursor.execute(
                    'SELECT timestamp, title, tally FROM timestamps '
                    f'WHERE {toggle_stamps_where} '
                    'ORDER BY timestamp ASC;').fetchall()
                timestamps_print = [
                    (indeces[i],
                     datetime.fromtimestamp(x[0]).strftime('%H:%M'),
                     x[1],
                     'Yes' if x[2] == 1 else 'No')
                    for i, x in enumerate(timestamps)]
                print("\n"
                      + tabulate(timestamps_print,
                                 headers=['', 'Time', 'Title', 'Tallied'],
                                 showindex=False))

                break
