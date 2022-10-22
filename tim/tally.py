from datetime import datetime
from os import path
import sqlite3
from tabulate import tabulate
import time

from tim.command import AbstractCommand


class TallyCommand(AbstractCommand):
    """Tally your day's work grouped by title."""

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

        for i in range(0, len(timestamps)):
            current = timestamps[i]
            next = current if i == len(timestamps) - 1 else timestamps[i + 1]
            timestamps[i] = (current + tuple([next[0] - current[0]]))

        timestamps = [(
                        datetime.fromtimestamp(x[0]).strftime('%H:%M'),
                        x[1],
                        self.seconds_to_time(x[2])
                    ) for x in timestamps]

        print(tabulate(timestamps, headers=['Time', 'Title', 'Duration'],
              showindex='always'))
        print('\n')
        print(tabulate(sorted(timestamps, key=lambda x: x[1]),
              headers=['Time', 'Title', 'Duration'],
              showindex='always'))

    def seconds_to_time(self, seconds: int) -> str:
        seconds = seconds % (24 * 3600)
        hour = seconds // 3600
        seconds %= 3600
        minutes = seconds // 60
        seconds %= 60
        if seconds > 29:
            minutes += 1

        return "%d:%02d" % (hour, minutes)
