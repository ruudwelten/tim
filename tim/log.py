from datetime import datetime
from os import path
import sqlite3
from tabulate import tabulate
from typing import Optional

from tim.command import AbstractCommand


class LogCommand(AbstractCommand):
    """Log today's timestmaps by default or a previous day with an offset."""

    signature: Optional[str] = "log"

    def run(self) -> None:
        print_index = False
        tim_dir = path.dirname(path.dirname(path.realpath(__file__)))
        db = path.join(tim_dir, 'db', 'tim.sqlite')
        conn = sqlite3.connect(db)
        cursor = conn.cursor()

        print(f'\033[1m\n\033[33m{self.printed_day}\033[0m\n')

        timestamps = cursor.execute(
            'SELECT timestamp, title FROM timestamps '
            f'WHERE timestamp >= {self.start} AND timestamp < {self.end} '
            'ORDER BY timestamp ASC;').fetchall()
        if len(timestamps) == 0:
            print('Oh no! Your log for this day looks empty ...\n'
                  '\n'
                  '\033[90m¯\\_(ツ)_/¯\033[0m\n'
                  '\n'
                  'To create a new timestamp run the following command:\n'
                  '\n'
                  '$ \033[1m\033[96mtim.py new [title]\033[0m')
            return

        timestamps_print = [
            (datetime.fromtimestamp(x[0]).strftime('%H:%M'), x[1])
            for x in timestamps]
        print(tabulate(timestamps_print, headers=['Time', 'Title'],
              showindex=print_index))
