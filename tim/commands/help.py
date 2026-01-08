from tim.commands import AbstractCommand
from tim.commands.registry import CommandRegistry
from tim.print import EBLUE, EBOLD, ECYAN, ERESET, EWHITE, EYELLOW


@CommandRegistry.register('help')
class HelpCommand(AbstractCommand):
    """Print instructions for Tim"""

    help_text = 'Show this help text'

    def run(self) -> None:
        self.print_ascii()

        print(f'\nUsage: {EBOLD}{EYELLOW}tim.py {ECYAN}[command] {EBLUE}[-#] '
              f'{ECYAN}[options]{ERESET} \n'
              '\n'
              f'{ECYAN}Commands:{ERESET}')

        registry = CommandRegistry()
        descriptions = registry.get_all_command_descriptions()

        # Calculate the maximum command name length for alignment
        max_command_length = max(len(cmd) for cmd in descriptions.keys())

        for command, description in descriptions.items():
            # Add padding to align descriptions
            padding = ' ' * (max_command_length - len(command))
            print(f'  {EBOLD}{command}{ERESET}{padding}    {description}')

    def print_ascii(self) -> None:
        print(f"\n\n{EBOLD}{EWHITE}"
              " .-') _          _   .-')\n"
              "(  OO) )        ( '.( OO )_\n"
              f"/     '._ {EYELLOW},-.{EWHITE}-') {EYELLOW},--.   ,--.{EWHITE})\n"
              f"{EYELLOW}|{EWHITE}'--...__){EYELLOW}|  |{EWHITE}OO){EYELLOW}|   `."
              "'   |\n"
              f"'--.  .--'|  |{EWHITE}  \\{EYELLOW}|         |\n"
              f"   |  |   |  |{EWHITE}(_/{EYELLOW}|  |'.'|  |\n"
              f"   |  |  {EWHITE},{EYELLOW}|  |{EWHITE}_.'{EYELLOW}|  |   |  |\n"
              f"   |  | {EWHITE}(_{EYELLOW}|  |   |  |   |  |\n"
              f"   `--'   `--'   `--'   `--'{ERESET}\n")
