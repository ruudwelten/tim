from abc import ABC, abstractmethod
from datetime import datetime, timedelta


class AbstractCommand(ABC):
    def __init__(self, args, day_offset):
        self.args = args
        self.day_offset = day_offset

        day = datetime.utcnow().date() + timedelta(self.day_offset)
        self.start = int(datetime.timestamp(datetime(day.year, day.month,
                                                     day.day)))
        self.end = int(datetime.timestamp(datetime(day.year, day.month,
                                                   day.day) + timedelta(1)))
        self.printed_day = day.strftime('%A, %d-%m-%Y')

    @abstractmethod
    def run(self) -> None:
        pass
