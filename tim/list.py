from datetime import datetime
from os import path
import sqlite3
from tabulate import tabulate
import time

from tim.command import AbstractCommand


class ListCommand(AbstractCommand):
    """List today's timestmaps by default or a previous day with an offset."""

    def run(self) -> None:
        print_index = False
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
              showindex=print_index))
