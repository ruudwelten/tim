from abc import ABC, abstractmethod
from datetime import datetime, timedelta, UTC
from pathlib import Path
import shutil
import tomli

from tim.db import DatabaseConnection


class AbstractCommand(ABC):
    def __init__(self, args, day_offset):
        self.args = args
        self.day_offset = day_offset

        self.read_config()

        self.set_day(datetime.now(UTC).date() + timedelta(self.day_offset))

        self.db = DatabaseConnection()

    def read_config(self) -> None:
        config_file = Path(__file__).parent.parent.parent / 'config.toml'
        example_config_file = (Path(__file__).parent.parent.parent
                               / 'config.example.toml')

        if not config_file.exists():
            print("Config file does not exist, creating one from example.")
            print("Edit config.toml to adjust the configuration.")
            shutil.copy(example_config_file, config_file)

        try:
            with open(config_file, mode='rb') as file:
                self.config = tomli.load(file)
        except FileNotFoundError:
            # Handle the case when the file does not exist
            print("Config file does not exist.")

    def set_day(self, day) -> None:
        self.day = day
        self.start = int(datetime.timestamp(datetime(day.year, day.month,
                                                     day.day)))
        self.end = int(datetime.timestamp(datetime(day.year, day.month,
                                                   day.day)
                                          + timedelta(1)))
        self.printed_day = day.strftime('%A, %d-%m-%Y')

    @abstractmethod
    def run(self) -> None:
        pass
