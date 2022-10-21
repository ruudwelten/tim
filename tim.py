#!/usr/bin/env python

import getopt
import re
import sys
import sqlite3
import time
from datetime import datetime
from os import path, remove, rename
from tabulate import tabulate


def main(argv):
    command = ''
    if len(argv) > 0 and argv[0] in ('help', 'today', 'init', 'new', 'list',
                                     'group'):
        command = argv[0]
        argv = argv[1:]

    if command == 'help':
        print_help()
    elif command == 'today':
        print_today()
        sys.exit(0)
    elif command == 'init':
        init()
    elif command == 'new':
        if len(argv) and argv[0][:1] != '-':
            new(argv[0], argv[1:])
        else:
            new('', argv)
    elif command == 'list':
        list()
    elif command == 'group':
        group()

    print_today()


def new(title='', argv=[]):
    try:
        opts, _ = getopt.getopt(argv, 'r:', ['retro='])
    except getopt.GetoptError:
        print_help(2)

    minute_delta = 0

    for opt, arg in opts:
        if opt == '-r':
            minute_delta = int(arg)

    timestamp = datetime.timestamp(datetime.now())
    timestamp = int(timestamp - minute_delta * 60)

    tim_dir = path.dirname(path.realpath(__file__))
    db = path.join(tim_dir, 'tim.sqlite')
    conn = sqlite3.connect(db)
    cursor = conn.cursor()
    cursor.execute(
        'INSERT INTO timestamps (timestamp, title) VALUES (?, ?);',
        [timestamp, title])
    conn.commit()
    sys.exit(0)


def list():
    tim_dir = path.dirname(path.realpath(__file__))
    db = path.join(tim_dir, 'tim.sqlite')
    conn = sqlite3.connect(db)
    cursor = conn.cursor()

    print('Today,', time.strftime('%d-%m-%Y'), '\n')

    timestamps = cursor.execute(
        "SELECT timestamp, title FROM timestamps "
        "WHERE timestamp >= strftime('%s', 'now', 'start of day') "
        "ORDER BY timestamp ASC;").fetchall()

    for i in range(0, len(timestamps)):
        current = timestamps[i]
        next = current if i == len(timestamps) - 1 else timestamps[i + 1]
        timestamps[i] = (current + tuple([next[0] - current[0]]))

    timestamps = [(
                      datetime.fromtimestamp(x[0]).strftime('%H:%M'),
                      x[1],
                      seconds_to_time(x[2])
                  ) for x in timestamps]

    print(tabulate(timestamps, headers=['Time', 'Title', 'Duration'],
                   showindex='always'))
    print('\n')
    print(tabulate(sorted(timestamps, key=lambda x: x[1]),
                   headers=['Time', 'Title', 'Duration'],
                   showindex='always'))

    sys.exit(0)


def group():
    timestamps = print_today(True)
    timestamps = [(x[0], datetime.fromtimestamp(x[0]).strftime('%H:%M'), x[1])
                  for x in timestamps]

    action = False
    while True:
        if action is not False:
            if re.fullmatch(r'([0-9]+, *)*[0-9]+', action) is None:
                print('The input is incorrect. Please supply the indeces of '
                      'the timestamps you want to group seperated by a comma. '
                      'Or q to quit.')
            else:
                indeces = [int(x.strip()) for x in action.split(',')]
                group_stamps = [timestamps[x] for x in indeces]

                print('\n')
                print(tabulate([[x[1], x[2]] for x in group_stamps],
                               headers=['Time', 'Title']))

                title = input('\nEnter a new title for these stamps: ')
                print(title)

        action = input('\nEnter the indeces to group (or q to quit): ')
        action = action.lower()

        if action == 'q':
            break

    sys.exit(0)


def seconds_to_time(seconds):
    seconds = seconds % (24 * 3600)
    hour = seconds // 3600
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60
    if seconds > 29:
        minutes += 1

    return "%d:%02d" % (hour, minutes)


def print_help(error=0):
    print('test.py -n <title> \n'
          '\n'
          'Commands:\n'
          'help    Show this help text\n'
          'new     Create new timestamp\n'
          'init    Initialize Tim database\n'
          'today   Show today\'s timestamps')
    sys.exit(error)


def print_today(print_index=False):
    tim_dir = path.dirname(path.realpath(__file__))
    db = path.join(tim_dir, 'tim.sqlite')
    conn = sqlite3.connect(db)
    cursor = conn.cursor()

    print('Today,', time.strftime('%d-%m-%Y'), '\n')

    timestamps = cursor.execute(
        "SELECT timestamp, title FROM timestamps "
        "WHERE timestamp >= strftime('%s', 'now', 'start of day') "
        "ORDER BY timestamp ASC;").fetchall()
    timestamps_print = [
        (datetime.fromtimestamp(x[0]).strftime('%H:%M'), x[1])
        for x in timestamps]
    print(tabulate(timestamps_print, headers=['Time', 'Title'],
                   showindex=print_index))

    return timestamps


def init():
    tim_dir = path.dirname(path.realpath(__file__))
    db = path.join(tim_dir, 'tim.sqlite')

    if path.isfile(db):
        action = input('There is already a database present, what do you want '
                       'to do? [b(ackup), r(emove), q(uit)]? ')
        action = action.lower()

        if action != 'b' and action != 'r':
            print('Quitting, database remains intact.')
            sys.exit(3)

        if action == 'b':
            now = time.strftime('%Y%m%d%H%M%S')
            rename(db, path.join(tim_dir, f'tim.{now}.sqlite'))

        if action == 'r':
            remove(db)

    open(db, 'a').close()

    conn = sqlite3.connect(db)
    cursor = conn.cursor()

    sql = open(path.join(tim_dir, 'init.sql'), 'r')
    initQueries = sql.read()
    sql.close()

    cursor.execute(initQueries)

    print(conn.total_changes, initQueries)

    sys.exit(0)


if __name__ == '__main__':
    main(sys.argv[1:])
