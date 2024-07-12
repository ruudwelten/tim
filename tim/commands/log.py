from tim.commands import AbstractCommand
from tim.print import print_log, print_heading


class LogCommand(AbstractCommand):
    """Log today's timestmaps by default or a previous day with an offset."""

    def run(self) -> None:
        print_heading(self.printed_day)

        timestamps = self.db.execute(
            'SELECT timestamp, title, tally FROM timestamps '
            f'WHERE timestamp >= {self.start} AND timestamp < {self.end} '
            'ORDER BY timestamp ASC;')

        print_log(timestamps)
