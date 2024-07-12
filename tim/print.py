from datetime import datetime
from tabulate import tabulate
from typing import Optional


def gray(test: str) -> str:
    return f'\033[90m{test}\033[0m'


def timestamp_to_time(timestamp: int) -> str:
    return datetime.fromtimestamp(timestamp).strftime('%H:%M')


def print_heading(text: str) -> None:
    print(f'\033[1m\n\033[33m{text}\033[0m\n')


def print_log(timestamps: list[int, str, Optional[bool]],
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

    tallied_timestamps_present = False
    for x in timestamps:
        if x[2] == 0:
            tallied_timestamps_present = True
            break
    if tallied_timestamps_present:
        print('\n\033[90m* Gray: Non tallied timestamps\033[0m')

    print('')
