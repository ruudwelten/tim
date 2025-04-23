from tim.commands import AbstractCommand
from tim.print import print_log, print_heading, colorize


class LogCommand(AbstractCommand):
    """Log today's timestmaps by default or a previous day with an offset."""

    def run(self) -> None:
        print_heading(self.printed_day)

        timestamps = self.db.cursor.execute(f'''
            SELECT t.timestamp, t.title, t.tally, p.color
            FROM timestamps t
            LEFT JOIN projects p
                ON SUBSTR(t.title, 1, INSTR(t.title, ' ')-1) = p.code
                    AND (t.timestamp >= p.start OR p.start IS NULL)
                    AND (t.timestamp <= p.end OR p.end IS NULL)
                    AND t.tally = 1
            WHERE t.timestamp >= {self.start} AND t.timestamp < {self.end}
            ORDER BY t.timestamp ASC;
        ''').fetchall()

        timestamps_print = [(
            x[0],
            (colorize(x[1].split(' ')[0], x[3]) + ' ' +
             ' '.join(x[1].split(' ')[1:]) if x[3] is not None else x[1]),
            x[2]
        ) for x in timestamps]

        print_log(timestamps_print)
