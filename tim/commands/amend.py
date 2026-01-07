from datetime import datetime

from tim.commands import AbstractCommand
from tim.commands.registry import CommandRegistry
from tim.print import print_heading, print_log


@CommandRegistry.register('amend')
class AmendCommand(AbstractCommand):
    """Rename the last timestamp"""

    def run(self) -> None:
        while True:
            timestamp = (self.db.execute(
                'SELECT timestamp, title FROM timestamps '
                'ORDER BY created DESC '
                'LIMIT 1;'))[0]
            print_heading(datetime.fromtimestamp(timestamp[0])
                                  .strftime('%A, %d-%m-%Y'),)
            print_log([timestamp])

            title = input(
                "\n\033[33mEnter a new title for this stamp: \033[0m")

            query = "UPDATE timestamps SET title = ? WHERE timestamp = ?;"
            self.db.execute(query, (title, timestamp[0]))
            self.db.commit()

            print("")

            timestamp = (self.db.execute(
                'SELECT timestamp, title FROM timestamps '
                'ORDER BY created DESC '
                'LIMIT 1;'))[0]
            print_log([timestamp])

            break
