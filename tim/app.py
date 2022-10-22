import re
import sys

from tim.command import AbstractCommand
from tim.group import GroupCommand
from tim.help import HelpCommand
from tim.init import InitCommand
from tim.list import ListCommand
from tim.new import NewCommand
from tim.tally import TallyCommand


def main() -> None:
    argv = sys.argv[1:]

    command = 'list'
    day_offset = 0

    if len(argv) > 0:
        if argv[0] in ('group', 'help', 'init', 'list', 'new', 'tally'):
            command = argv[0]
            argv = argv[1:]
        else:
            command = 'list'

        if len(argv) > 0 and re.fullmatch(r'[-+][0-9]+', argv[0]):
            day_offset = int(argv[0])

    commandClass: AbstractCommand = HelpCommand(argv, day_offset)
    if command == 'group':
        commandClass = GroupCommand(argv, day_offset)
    elif command == 'help':
        commandClass = HelpCommand(argv, day_offset)
    elif command == 'init':
        commandClass = InitCommand(argv, day_offset)
    elif command == 'list':
        commandClass = ListCommand(argv, day_offset)
    elif command == 'new':
        commandClass = NewCommand(argv, day_offset)
    elif command == 'tally':
        commandClass = TallyCommand(argv, day_offset)

    commandClass.run()


if __name__ == "__main__":
    main()
