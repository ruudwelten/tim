from abc import ABC, abstractmethod
from datetime import datetime, timedelta
from pathlib import Path
import tomli
from typing import Optional
import shutil


class AbstractCommand(ABC):
    signature: Optional[str] = None

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
        config_file = Path(__file__).parent.parent / 'config.toml'
        example_config_file = Path(__file__).parent.parent / 'config.example.toml'

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

    @abstractmethod
    def run(self) -> None:
        pass
