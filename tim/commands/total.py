from datetime import datetime
from os import path
import sqlite3

from tim import TIM_DIR
from tim.commands import AbstractCommand


class TotalCommand(AbstractCommand):
    """Output the total tally of your day's work."""

    def run(self) -> None:
        db = path.join(TIM_DIR, 'db', 'tim.sqlite')
        conn = sqlite3.connect(db)
        cursor = conn.cursor()

        print(f'\033[1m\n\033[33m{self.printed_day}\033[0m\n')

        timestamps = cursor.execute(
            'SELECT timestamp, title, tally FROM timestamps '
            f'WHERE timestamp >= {self.start} AND timestamp < {self.end} '
            'ORDER BY timestamp ASC;').fetchall()

        # When the last timestamp is tallied, tally the time up to "now"
        latest_timestamp = timestamps[-1]
        if latest_timestamp[2] == 1:
            timestamps.append((datetime.now().timestamp(), 'Now', 0))

        total_time = 0
        for i in range(0, len(timestamps)):
            current = timestamps[i]
            next = current if i == len(timestamps) - 1 else timestamps[i + 1]
            time = next[0] - current[0]
            timestamps[i] = (current + tuple([time]))
            if timestamps[i][2] > 0:
                total_time += time

        print(f'Total: {self.seconds_to_time(total_time)}')

    def seconds_to_time(self, seconds: int) -> str:
        seconds = seconds % (24 * 3600)
        hour = seconds // 3600
        seconds %= 3600
        minutes = seconds // 60
        seconds %= 60
        if seconds > 29:
            minutes += 1

        return "%d:%02d" % (hour, minutes)
