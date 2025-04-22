from typing import Dict, Type, Optional, NamedTuple
from importlib import import_module
from .abstract import AbstractCommand


class CommandInfo(NamedTuple):
    module_path: str
    description: str


class CommandRegistry:
    _instance = None
    _commands: Dict[str, Type[AbstractCommand]] = {}
    _command_info = {
        'amend': CommandInfo('tim.commands.amend', 'Rename the last timestamp'),
        'group': CommandInfo('tim.commands.group', 'Group timestamps under the same title'),
        'help': CommandInfo('tim.commands.help', 'Show this help text'),
        'init': CommandInfo('tim.commands.init', 'Initialize Tim, creates database'),
        'log': CommandInfo('tim.commands.log', 'Show a day\'s timestamps'),
        'new': CommandInfo('tim.commands.new', 'Create new timestamp'),
        'project': CommandInfo('tim.commands.project', 'Manage projects'),
        'rename': CommandInfo('tim.commands.rename', 'Rename timestamp'),
        'tally': CommandInfo('tim.commands.tally', 'Show a day\'s time tally'),
        'toggle': CommandInfo('tim.commands.toggle', 'Toggle the tally status of a timestamp'),
        'total': CommandInfo('tim.commands.total', 'Output the total tally of your day\'s work')
    }

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(CommandRegistry, cls).__new__(cls)
        return cls._instance

    def get_command(self, command_name: str) -> Optional[Type[AbstractCommand]]:
        """Get a command class by name, loading it if necessary."""
        if command_name not in self._commands:
            if command_name not in self._command_info:
                return None

            module_path = self._command_info[command_name].module_path
            module = import_module(module_path)
            command_class = getattr(module, f"{command_name.title()}Command")
            self._commands[command_name] = command_class

        return self._commands[command_name]

    def get_available_commands(self) -> list[str]:
        """Get a list of all available command names."""
        return list(self._command_info.keys())

    def get_command_description(self, command_name: str) -> Optional[str]:
        """Get the description for a command."""
        if command_name in self._command_info:
            return self._command_info[command_name].description
        return None

    def get_all_command_descriptions(self) -> Dict[str, str]:
        """Get descriptions for all commands."""
        return {name: info.description for name, info in self._command_info.items()}
