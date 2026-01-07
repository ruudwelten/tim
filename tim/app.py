import re
import sys
from typing import Optional, Tuple

from tim.commands.registry import CommandRegistry


def main() -> None:
    try:
        argv = sys.argv[1:]

        command = 'log'
        day_offset = 0

        command, argv = extract_command(argv)
        day_offset, argv = extract_day_offset(argv)

        registry = CommandRegistry()
        try:
            command_class = registry.get_command(command or 'help')
        except KeyError:
            print(f"\033[31mUnknown command: {command}\033[0m")
            command_class = registry.get_command('help')

        command_instance = command_class(argv, day_offset)
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
