from typing import Dict, Type, Optional
from importlib import import_module
from .abstract import AbstractCommand

class CommandRegistry:
    _instance = None
    _commands: Dict[str, Type[AbstractCommand]] = {}
    _command_modules = {
        'amend': 'tim.commands.amend',
        'group': 'tim.commands.group',
        'help': 'tim.commands.help',
        'init': 'tim.commands.init',
        'log': 'tim.commands.log',
        'new': 'tim.commands.new',
        'rename': 'tim.commands.rename',
        'tally': 'tim.commands.tally',
        'toggle': 'tim.commands.toggle',
        'total': 'tim.commands.total'
    }

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(CommandRegistry, cls).__new__(cls)
        return cls._instance

    def get_command(self, command_name: str) -> Optional[Type[AbstractCommand]]:
        """Get a command class by name, loading it if necessary."""
        if command_name not in self._commands:
            if command_name not in self._command_modules:
                return None

            module_path = self._command_modules[command_name]
            module = import_module(module_path)
            command_class = getattr(module, f"{command_name.title()}Command")
            self._commands[command_name] = command_class

        return self._commands[command_name]

    def get_available_commands(self) -> list[str]:
        """Get a list of all available command names."""
        return list(self._command_modules.keys())
