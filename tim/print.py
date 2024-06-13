from datetime import datetime
from tabulate import tabulate
from typing import Optional


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
    timestamps_print = [
        (datetime.fromtimestamp(x[0]).strftime('%H:%M'), x[1])
        for x in timestamps]
    if len(timestamps[0]) > 2:
        headers.append('Tallied')
        timestamps_print = [timestamps_print[i]
                            + ('Yes' if x[2] == 1 else 'No',)
                            for i, x in enumerate(timestamps)]

    print(tabulate(timestamps_print, headers=headers,
          showindex=print_index))
