from typing import Callable, Dict, NamedTuple, Type

from .abstract import AbstractCommand


class CommandMeta(NamedTuple):
    name: str
    description: str
    command_class: Type[AbstractCommand]


class CommandRegistry:
    _instance = None
    _commands: Dict[str, CommandMeta] = {}

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(CommandRegistry, cls).__new__(cls)
        return cls._instance

    @classmethod
    def register(cls, name: str) -> Callable[[Type[AbstractCommand]], Type[AbstractCommand]]:
        """Decorator to register a command class."""
        def decorator(command_class: Type[AbstractCommand]) -> Type[AbstractCommand]:
            cls._commands[name] = CommandMeta(
                name,
                command_class.help_text or command_class.__doc__ or "-",
                command_class
            )
            return command_class
        return decorator

    def get_command(self, command_name: str, argv: list = list(), day_offset: int = 0) -> AbstractCommand:
        """Get a command instance by name."""
        if command_name not in self._commands:
            raise KeyError(f"Unknown command: {command_name}")
        return self._commands[command_name].command_class(argv, day_offset)

    def get_available_commands(self) -> list[str]:
        """Get a list of all available command names."""
        return list(self._commands.keys())

    def get_command_description(self, command_name: str) -> str:
        """Get the description for a command."""
        if command_name not in self._commands:
            raise KeyError(f"Unknown command: {command_name}")
        return self._commands[command_name].description

    def get_all_command_descriptions(self) -> Dict[str, str]:
        """Get descriptions for all commands."""
        return {name: meta.description for name, meta in self._commands.items()}
