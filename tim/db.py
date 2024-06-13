from os import path
import sqlite3

from tim import TIM_DIR


class DatabaseConnection:
    def __init__(self):
        self.db = path.join(TIM_DIR, 'db', 'tim.sqlite')
        self.conn = sqlite3.connect(self.db)
        self.cursor = self.conn.cursor()

    def commit(self) -> None:
        self.conn.commit()

    def execute(self, query: str) -> list:
        return self.cursor.execute(query).fetchall()
