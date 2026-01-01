import sqlite3
from os import path

from tim import TIM_DIR


class DatabaseConnection:
    def __init__(self):
        self.db = path.join(TIM_DIR, "db", "tim.sqlite")
        self.conn = sqlite3.connect(self.db)
        self.cursor = self.conn.cursor()

    def commit(self) -> None:
        self.conn.commit()

    def execute(self, query: str, params: tuple = ()) -> list:
        return self.cursor.execute(query, params).fetchall()
