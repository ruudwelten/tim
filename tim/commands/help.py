from tim.commands import AbstractCommand
from tim.commands.registry import CommandRegistry


class HelpCommand(AbstractCommand):
    """Print instructions for Tim."""

    def run(self) -> None:
        self.print_ascii()

        print('\nUsage: \033[1m\033[33mtim.py \033[36m[command] \033[34m[-#] '
              '\033[36m[options]\033[0m \n'
              '\n'
              '\033[36mCommands:\033[0m')

        registry = CommandRegistry()
        descriptions = registry.get_all_command_descriptions()

        # Calculate the maximum command name length for alignment
        max_command_length = max(len(cmd) for cmd in descriptions.keys())

        for command, description in descriptions.items():
            # Add padding to align descriptions
            padding = ' ' * (max_command_length - len(command))
            print(f'  \033[1m{command}\033[0m{padding}    {description}')

    def print_ascii(self) -> None:
        bold = '\033[1m'
        y = '\033[33m'
        w = '\033[97m'
        r = '\033[0m'
        print(f"\n\n{bold}{w}"
              f" .-') _          _   .-')\n"
              f"(  OO) )        ( '.( OO )_\n"
              f"/     '._ {y},-.{w}-') {y},--.   ,--.{w})\n"
              f"{y}|{w}'--...__){y}|  |{w}OO){y}|   `."
              f"'   |\n"
              f"'--.  .--'|  |{w}  \\{y}|         |\n"
              f"   |  |   |  |{w}(_/{y}|  |'.'|  |\n"
              f"   |  |  {w},{y}|  |{w}_.'{y}|  |   |  |\n"
              f"   |  | {w}(_{y}|  |   |  |   |  |\n"
              f"   `--'   `--'   `--'   `--'{r}\n")
