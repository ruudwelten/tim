from datetime import datetime
from typing import Dict, Optional

from tabulate import tabulate

# ANSI color codes
BOLD = 1
BLACK = 30
RED = 31
GREEN = 32
YELLOW = 33
BLUE = 34
MAGENTA = 35
CYAN = 36
WHITE = 37
GRAY = 90
BRIGHT_RED = 91
BRIGHT_GREEN = 92
BRIGHT_YELLOW = 93
BRIGHT_BLUE = 94
BRIGHT_MAGENTA = 95
BRIGHT_CYAN = 96
BRIGHT_WHITE = 97
COLORS: Dict[int, str] = {
    BLACK: 'Black',
    RED: 'Red',
    GREEN: 'Green',
    YELLOW: 'Yellow',
    BLUE: 'Blue',
    MAGENTA: 'Magenta',
    CYAN: 'Cyan',
    WHITE: 'White',
    GRAY: 'Gray',
    BRIGHT_RED: 'Bright Red',
    BRIGHT_GREEN: 'Bright Green',
    BRIGHT_YELLOW: 'Bright Yellow',
    BRIGHT_BLUE: 'Bright Blue',
    BRIGHT_MAGENTA: 'Bright Magenta',
}


def gray(text: str) -> str:
    return colorize(text, GRAY)


def colorize(text: str, color_code: int, bold: bool = False) -> str:
    codes = [color_code]
    if bold:
        codes.append(BOLD)
    return f'\033[{";".join(str(c) for c in codes)}m{text}\033[0m'


def timestamp_to_time(timestamp: int) -> str:
    return datetime.fromtimestamp(timestamp).strftime('%H:%M')


def print_heading(text: str) -> None:
    print(f'\n{colorize(text, YELLOW, bold=True)}\n')


def print_success(text: str) -> None:
    print(f'\n{colorize(text, GREEN, bold=True)}\n')


def print_error(text: str) -> None:
    print(f'\n{colorize(text, RED, bold=True)}\n')


def print_log(timestamps: list[tuple[int, str, Optional[bool]]],
              print_index: bool = False) -> None:
    if len(timestamps) == 0:
        print('Oh no! Your log for this day looks empty ...\n'
              '\n'
              '\033[90m¯\\_(ツ)_/¯\033[0m\n'
              '\n'
              'To create a new timestamp run the following command:\n'
              '\n'
              '$ \033[1m\033[96mtim.py new [title]\033[0m')
        return

    headers = ['Time', 'Title']

    if len(timestamps[0]) > 2:
        timestamps_print = [(timestamp_to_time(x[0])
                             if x[2] == 1
                             else gray(timestamp_to_time(x[0])),
                             x[1] if x[2] == 1 else gray(x[1]))
                            for x in timestamps]
    else:
        timestamps_print = [(timestamp_to_time(x[0]), x[1])
                            for x in timestamps]

    print(tabulate(timestamps_print, headers=headers, showindex=print_index))

    if len(timestamps[0]) > 2:
        tallied_timestamps_present = False
        for x in timestamps:
            if x[2] == 0:
                tallied_timestamps_present = True
                break
        if tallied_timestamps_present:
            print(f'\n{gray("* Gray: Non tallied timestamps")}')

    print('')
