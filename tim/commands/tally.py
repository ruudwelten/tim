from datetime import datetime, timedelta
from tabulate import tabulate, SEPARATING_LINE

from tim.commands import AbstractCommand


class TallyCommand(AbstractCommand):
    """Tally your day's work grouped by title."""

    def run(self) -> None:
        if self.week_flag_is_set():
            self.tally_week()
        else:
            self.tally_day()

        self.read_config()

    def week_flag_is_set(self) -> bool:
        return '-w' in self.args

    def tally_day(self) -> None:
        print(f'\033[1m\n\033[33m{self.printed_day}\033[0m\n')

        timestamps = self.db.cursor.execute(
            'SELECT timestamp, title, tally FROM timestamps '
            f'WHERE timestamp >= {self.start} AND timestamp < {self.end} '
            'ORDER BY timestamp ASC;').fetchall()

        if len(timestamps) == 0:
            print('No timestamps on this day.')
            return

        # When the last timestamp is tallied, tally the time up to "now"
        ongoing = False
        latest_timestamp = timestamps[-1]
        if latest_timestamp[2] == 1:
            ongoing = True
            timestamps.append((datetime.now().timestamp(), 'Now', 0))

        total_time = 0
        untallied_timestamps_to_remove = []
        for i in range(0, len(timestamps)):
            current = timestamps[i]
            next = current if i == len(timestamps) - 1 else timestamps[i + 1]
            time = next[0] - current[0]
            timestamps[i] = (current + tuple([time]))
            if timestamps[i][2] == 0:
                untallied_timestamps_to_remove.append(i)
            else:
                total_time += time

        untallied_timestamps_to_remove.sort(reverse=True)
        for index in untallied_timestamps_to_remove:
            del timestamps[index]

        timestamps.sort(key=lambda x: x[1])

        duplicate_timestamps_to_remove = []
        for i in range(1, len(timestamps)):
            previous = timestamps[i - 1]
            current = timestamps[i]
            if (previous[1] == current[1]):
                timestamps[i] = (current[0], current[1], current[2],
                                 current[3] + previous[3])
                duplicate_timestamps_to_remove.append(i - 1)

        duplicate_timestamps_to_remove.sort(reverse=True)
        for index in duplicate_timestamps_to_remove:
            del timestamps[index]

        timestamps_print = [(x[1],
                             self.seconds_to_time(x[3]) +
                             (' (ongoing)'
                              if ongoing and x[1] == latest_timestamp[1]
                              else ''))
                            for x in timestamps]
        timestamps_print.append(SEPARATING_LINE)
        timestamps_print.append(tuple(['Total',
                                self.seconds_to_time(total_time)]))

        print(tabulate(timestamps_print,
                       headers=['Title', 'Duration'],
                       showindex=False))

    def tally_week(self):
        monday = self.day - timedelta(days=self.day.weekday())
        for i in range(0, 7):
            self.set_day(monday + timedelta(days=i))
            self.tally_day()

    def seconds_to_time(self, seconds: int) -> str:
        seconds = seconds % (24 * 3600)
        hour = seconds // 3600
        seconds %= 3600
        minutes = seconds // 60
        seconds %= 60
        if seconds > 29:
            minutes += 1

        return "%d:%02d" % (hour, minutes)
