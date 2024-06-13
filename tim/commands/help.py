from tim.commands import AbstractCommand


class HelpCommand(AbstractCommand):
    """Print instructions for Tim."""

    def run(self) -> None:
        self.print_ascii()

        print('\nUsage: \033[1m\033[33mtim.py \033[36m[command] \033[34m[-#] '
              '\033[36m[options]\033[0m \n'
              '\n'
              '\033[36mCommands:\033[0m\n'
              '  \033[1mhelp\033[0m    Show this help text\n'
              '  \033[1mgroup\033[0m   Group timestamps under the same title\n'
              '  \033[1minit\033[0m    Initialize Tim, creates database\n'
              '  \033[1mlog\033[0m     Show a day\'s timestamps\n'
              '  \033[1mnew\033[0m     Create new timestamp\n'
              '  \033[1mtally\033[0m   Show a day\'s time tally')

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
