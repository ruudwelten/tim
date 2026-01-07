import re
from datetime import datetime

from tabulate import tabulate

from tim.commands import AbstractCommand
from tim.commands.registry import CommandRegistry
from tim.print import YELLOW, colorize, print_heading, print_log


@CommandRegistry.register('rename')
class RenameCommand(AbstractCommand):
    """Rename timestamp"""

    def run(self) -> None:
        while True:
            print_heading(self.printed_day)

            timestamps = self.db.execute(
                'SELECT timestamp, title, tally FROM timestamps '
                f'WHERE timestamp >= {self.start} AND timestamp < {self.end} '
                'ORDER BY timestamp ASC;')
            print_log(timestamps, True)

            timestamps = [
                (x[0],
                 datetime.fromtimestamp(x[0]).strftime('%H:%M'),
                 x[1],
                 x[2])
                for x in timestamps
            ]

            index = input(colorize('\nEnter the index of the timestamp to '
                                   'rename (or q to quit):', YELLOW))
            index = index.lower()

            if index == 'q':
                break

            if re.fullmatch(r'[0-9]+', index) is None:
                print('The input is incorrect. Please supply the index of the '
                      'timestamps you want to rename.')
            else:
                rename_stamp = timestamps[int(index)]

                print('\n')
                print(tabulate([[rename_stamp[1], rename_stamp[2]]],
                               headers=['Time', 'Title']))

                title = input(colorize('\nEnter a new title for this stamp:',
                                       YELLOW))

                query = f'''UPDATE timestamps SET title = \'{title}\'
                            WHERE timestamp = {rename_stamp[0]};'''
                self.db.execute(query)
                self.db.commit()

                timestamps = self.db.execute(
                    'SELECT timestamp, title, tally FROM timestamps '
                    f'WHERE timestamp = {rename_stamp[0]} '
                    'ORDER BY timestamp ASC;')
                timestamps_print = [
                    (index,
                     datetime.fromtimestamp(x[0]).strftime('%H:%M'),
                     x[1],
                     'Yes' if x[2] == 1 else 'No')
                    for i, x in enumerate(timestamps)]
                print("\n" + tabulate(timestamps_print,
                                      headers=['', 'Time', 'Title', 'Tallied'],
                                      showindex=False))

                break
