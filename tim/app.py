import re
import sys
from typing import Tuple, Optional

from tim.commands import (
    AbstractCommand, AmendCommand, GroupCommand, HelpCommand, InitCommand,
    LogCommand, NewCommand, RenameCommand, TallyCommand, ToggleCommand,
    TotalCommand
)


def main() -> None:
    argv = sys.argv[1:]

    command = 'log'
    day_offset = 0

    command, argv = extract_command(argv)
    day_offset, argv = extract_day_offset(argv)

    commandClass: AbstractCommand = HelpCommand(argv, day_offset)
    if command == 'amend':
        commandClass = AmendCommand(argv, day_offset)
    elif command == 'group':
        commandClass = GroupCommand(argv, day_offset)
    elif command == 'init':
        commandClass = InitCommand(argv, day_offset)
    elif command == 'log':
        commandClass = LogCommand(argv, day_offset)
    elif command == 'new':
        commandClass = NewCommand(argv, day_offset)
    elif command == 'rename':
        commandClass = RenameCommand(argv, day_offset)
    elif command == 'tally':
        commandClass = TallyCommand(argv, day_offset)
    elif command == 'toggle':
        commandClass = ToggleCommand(argv, day_offset)
    elif command == 'total':
        commandClass = TotalCommand(argv, day_offset)

    commandClass.run()


def extract_command(argv) -> Tuple[Optional[str], list]:
    if len(argv) == 0:
        return (None, argv)

    if argv[0] in ('amend', 'group', 'help', 'init', 'log', 'new', 'rename',
                   'tally', 'toggle', 'total'):
        return (argv[0], argv[1:])

    return (None, argv)


def extract_day_offset(argv) -> Tuple[int, list]:
    if len(argv) == 0:
        return (0, argv)

    pattern = re.compile(r'[-+][0-9]+')
    offset_flags = list(filter(pattern.match, argv))
    argv = [x for x in argv if x not in offset_flags]

    if len(offset_flags) == 0:
        return (0, argv)

    return int(offset_flags[-1:][0]), argv


if __name__ == "__main__":
    main()
