from abc import ABC, abstractmethod


class AbstractCommand(ABC):
    def __init__(self, args, day_offset):
        self.args = args
        self.day_offset = day_offset

    @abstractmethod
    def run(self) -> None:
        pass
