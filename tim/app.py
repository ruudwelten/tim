import re
import sys
from typing import Tuple, Optional

from tim.commands import (
    AbstractCommand, GroupCommand, HelpCommand, InitCommand, LogCommand,
    NewCommand, TallyCommand, ToggleCommand
)


def main() -> None:
    argv = sys.argv[1:]

    command = 'log'
    day_offset = 0

    command, argv = extract_command(argv)
    day_offset, argv = extract_day_offset(argv)

    commandClass: AbstractCommand = HelpCommand(argv, day_offset)
    if command == 'group':
        commandClass = GroupCommand(argv, day_offset)
    elif command == 'init':
        commandClass = InitCommand(argv, day_offset)
    elif command == 'log':
        commandClass = LogCommand(argv, day_offset)
    elif command == 'new':
        commandClass = NewCommand(argv, day_offset)
    elif command == 'tally':
        commandClass = TallyCommand(argv, day_offset)
    elif command == 'toggle':
        commandClass = ToggleCommand(argv, day_offset)

    commandClass.run()


def extract_command(argv) -> Tuple[Optional[str], list]:
    if len(argv) == 0:
        return (None, argv)

    if argv[0] in ('group', 'help', 'init', 'log', 'new', 'tally', 'toggle'):
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
