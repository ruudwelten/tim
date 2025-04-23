from os import path, remove, rename
import sqlite3
import sys
import time

from tim import TIM_DIR
from tim.commands import AbstractCommand
from tim.print import colorize, print_success, YELLOW


class InitCommand(AbstractCommand):
    """Initialize Tim, creates new database."""

    def run(self) -> None:
        db = path.join(TIM_DIR, 'db', 'tim.sqlite')

        if path.isfile(db):
            action = input(colorize('\nThere is already a database present, '
                                    'what do you want to do? '
                                    '[b(ackup), r(emove), q(uit)]? ',
                                    YELLOW))
            action = action.lower()

            if action != 'b' and action != 'r':
                print('Quitting, database remains intact.')
                sys.exit(3)

            if action == 'b':
                now = time.strftime('%Y%m%d%H%M%S')
                backup_path = path.join(TIM_DIR, 'db', f'tim.{now}.sqlite')
                rename(db, backup_path)

                print(f'Backup created at {backup_path}')

            if action == 'r':
                remove(db)

        open(db, 'a').close()

        conn = sqlite3.connect(db)
        cursor = conn.cursor()

        sql = open(path.join(TIM_DIR, 'init.sql'), 'r')
        initQueries = sql.read()
        sql.close()

        queryLines = [x for x in initQueries.split('\n')
                          if x.strip() and not x.strip().startswith('--')]
        queries = '\n'.join(queryLines).split(';')

        # Execute each query separately
        for query in queries:
            try:
                cursor.execute(query)
            except Exception as e:
                print(f"Error executing query: {query}")
                print(f"Error details: {str(e)}")
                raise

        print_success('Tim database initialized')
