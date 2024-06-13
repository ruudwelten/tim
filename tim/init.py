from os import path, remove, rename
import sqlite3
import sys
import time

from tim import TIM_DIR
from tim.command import AbstractCommand


class InitCommand(AbstractCommand):
    """Initialize Tim, creates new database."""

    def run(self) -> None:
        db = path.join(TIM_DIR, 'db', 'tim.sqlite')

        if path.isfile(db):
            action = input('There is already a database present, what do you '
                           'want to do? [b(ackup), r(emove), q(uit)]? ')
            action = action.lower()

            if action != 'b' and action != 'r':
                print('Quitting, database remains intact.')
                sys.exit(3)

            if action == 'b':
                now = time.strftime('%Y%m%d%H%M%S')
                rename(db, path.join(TIM_DIR, 'db', f'tim.{now}.sqlite'))

            if action == 'r':
                remove(db)

        open(db, 'a').close()

        conn = sqlite3.connect(db)
        cursor = conn.cursor()

        sql = open(path.join(TIM_DIR, 'init.sql'), 'r')
        initQueries = sql.read()
        sql.close()

        cursor.execute(initQueries)

        print(conn.total_changes, initQueries)
