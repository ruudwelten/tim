from abc import ABC, abstractmethod
from datetime import datetime, timedelta
from pathlib import Path
import tomli


class AbstractCommand(ABC):
    def __init__(self, args, day_offset):
        self.args = args
        self.day_offset = day_offset

        self.read_config()

        day = datetime.utcnow().date() + timedelta(self.day_offset)
        self.start = int(datetime.timestamp(datetime(day.year, day.month,
                                                     day.day)))
        self.end = int(datetime.timestamp(datetime(day.year, day.month,
                                                   day.day) + timedelta(1)))
        self.printed_day = day.strftime('%A, %d-%m-%Y')

    def read_config(self) -> None:
        with open(Path(__file__).parent.parent / 'config.toml', mode='rb') as file:
            self.config = tomli.load(file)

    @abstractmethod
    def run(self) -> None:
        pass
