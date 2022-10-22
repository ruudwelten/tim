from tim.command import AbstractCommand


class HelpCommand(AbstractCommand):
    """Print instructions for Tim."""

    def run(self) -> None:
        print('\nUsage: \033[1m\033[33mtim.py \033[36m[command] \033[34m[-#] '
              '\033[36m[options]\033[0m \n'
              '\n'
              '\033[36mCommands:\033[0m\n'
              '  \033[1mhelp\033[0m    Show this help text\n'
              '  \033[1mgroup\033[0m   Group timestamps under the same title\n'
              '  \033[1minit\033[0m    Initialize Tim, creates database\n'
              '  \033[1mlist\033[0m    Show a day\'s timestamps\n'
              '  \033[1mnew\033[0m     Create new timestamp\n'
              '  \033[1mtally\033[0m   Show a day\'s time tally')
