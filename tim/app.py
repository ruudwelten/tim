import re
import sys
from typing import Optional, Tuple

from tim.commands import (  # noqa: F401
    amend,
    group,
    help,
    init,
    log,
    new,
    project,
    rename,
    tally,
    toggle,
    total,
)
from tim.commands.registry import CommandRegistry
from tim.print import RED, colorize


def main() -> None:
    try:
        argv = sys.argv[1:]

        command = 'log'
        day_offset = 0

        command, argv = extract_command(argv)
        day_offset, argv = extract_day_offset(argv)

        registry = CommandRegistry()
        try:
            command_instance = registry.get_command(command or 'help',
                                                    argv, day_offset)
        except KeyError:
            print(colorize(f"\nUnknown command: {command}", RED, True))
            command_instance = registry.get_command('help')

        command_instance.run()
    except KeyboardInterrupt:
        print()
        sys.exit(0)


def extract_command(argv) -> Tuple[Optional[str], list]:
    if len(argv) == 0:
        return (None, argv)
    return (argv[0], argv[1:])


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
