import argparse
from datetime import datetime
from typing import Optional

from tabulate import tabulate

from tim.commands import AbstractCommand
from tim.commands.registry import CommandRegistry
from tim.print import COLORS, YELLOW, colorize, gray, print_heading, print_success


@CommandRegistry.register('project')
class ProjectCommand(AbstractCommand):
    """Manage projects"""

    def __init__(self, args, day_offset):
        super(ProjectCommand, self).__init__(args, day_offset)
        self.parser = self.setup_parser()
        self.args = self.parser.parse_args(args)

    def setup_parser(self) -> argparse.ArgumentParser:
        parser = argparse.ArgumentParser(prog='tim project',
                                         description='Manage projects')
        subparsers = parser.add_subparsers(dest='action',
                                           help='Action to perform')

        # Add project
        subparsers.add_parser('new', help='Create a new project')

        # List projects
        list_parser = subparsers.add_parser('list', help='List all projects')
        list_parser.add_argument(
            '-a',
            '--all',
            action='store_true',
            help='Show all projects, including past and future ones'
        )

        # Edit project
        edit_parser = subparsers.add_parser('edit', help='Edit a project')
        edit_parser.add_argument('code', help='Project code to edit')

        # Remove project
        remove_parser = subparsers.add_parser('remove',
                                              help='Remove a project')
        remove_parser.add_argument('code', help='Project code to remove')

        # Colors
        subparsers.add_parser('colors', help='Show available colors')

        return parser

    def run(self) -> None:
        if not self.args.action:
            self.parser.print_help()
            return

        if self.args.action == 'new':
            self.add_project()
        elif self.args.action == 'list':
            self.list_projects()
        elif self.args.action == 'edit':
            self.edit_project()
        elif self.args.action == 'remove':
            self.remove_project()
        elif self.args.action == 'colors':
            self.show_colors()

    def parse_date(self, date_str: Optional[str]) -> Optional[int]:
        if not date_str:
            return None
        try:
            return int(datetime.strptime(date_str, '%Y-%m-%d').timestamp())
        except ValueError:
            print(gray(f"Invalid date format: {date_str}. Use YYYY-MM-DD"))
            return None

    def add_project(self) -> None:
        """Interactive project creation."""
        print_heading("Create Project")

        # Get project name
        while True:
            name = input("Project name: ").strip()
            if name:
                break
            print(gray("Project name cannot be empty."))

        # Get project code
        while True:
            code = input("Project code (e.g., 'ABC'): ").strip().upper()
            if code:
                # Check if code already exists
                existing = self.db.cursor.execute(
                    'SELECT code FROM projects WHERE code = ?',
                    [code]
                ).fetchall()
                if existing:
                    print(gray(f"Project code '{code}' already exists."))
                    continue
                break
            print(gray("Project code cannot be empty."))

        # Get color
        self.show_colors()
        while True:
            color_input = input(f"Color code [37]: ").strip()
            if not color_input:
                color = 37
                break
            try:
                color = int(color_input)
                if color in COLORS:
                    break
                print(gray(
                    f"Invalid color code. Please choose from: {', '.join(str(c) for c in COLORS.keys())}"))
            except ValueError:
                print(gray("Please enter a valid number."))

        # Get start date
        while True:
            start = input("Start date (YYYY-MM-DD, or leave empty): ").strip()
            if not start:
                start_timestamp = None
                break
            start_timestamp = self.parse_date(start)
            if start_timestamp is not None:
                break

        # Get end date
        while True:
            end = input("End date (YYYY-MM-DD, or leave empty): ").strip()
            if not end:
                end_timestamp = None
                break
            end_timestamp = self.parse_date(end)
            if end_timestamp is not None:
                break

        # Save
        self.save_project(code, name, color, start_timestamp, end_timestamp)
        print_success(f"Project {name} ({code}) created successfully")

    def list_projects(self) -> None:
        now = int(datetime.now().timestamp())
        query = '''
            SELECT code, name, color, start, end
            FROM projects
            ORDER BY code
        '''
        projects = self.db.cursor.execute(query).fetchall()

        if not projects:
            print(gray("No projects found."))
            return

        # Filter projects based on current date if --all is not specified
        if not self.args.all:
            current_projects = []
            non_current_projects = []
            for project in projects:
                start = project[3] or 0
                end = project[4] or float('inf')
                if start <= now <= end:
                    current_projects.append(project)
                else:
                    non_current_projects.append(project)
            projects = current_projects
        else:
            non_current_projects = []

        if not projects:
            print(gray("No current projects found."))
            if non_current_projects:
                print(gray("\nUse 'tim project list --all' to see all "
                           "projects."))
            return

        # Format the projects for display
        formatted_projects = []
        for project in projects:
            project_code = colorize(project[0], project[2])
            project_name = colorize(project[1], project[2])
            start_date = datetime.fromtimestamp(project[3]).strftime(
                '%Y-%m-%d') if project[3] else gray('---')
            end_date = datetime.fromtimestamp(project[4]).strftime(
                '%Y-%m-%d') if project[4] else gray('---')
            formatted_projects.append(
                (project_code, project_name, start_date, end_date))

        print_heading("All projects" if self.args.all else "Current projects")
        print(tabulate(formatted_projects,
                       headers=['Code', 'Name', 'Start', 'End'],
                       showindex=False))

        if non_current_projects and not self.args.all:
            print(gray("\nUse 'tim project list --all' to see all projects."))

    def edit_project(self) -> None:
        """Interactive project editing."""
        # First check if project exists
        project = self.db.cursor.execute('''
            SELECT code, name, color, start, end
            FROM projects
            WHERE code = ?
        ''', [self.args.code]).fetchall()

        if not project:
            print(gray(f"Project {self.args.code} not found."))
            return

        project = project[0]  # Get the first (and should be only) result
        current_name = project[1]
        current_color = project[2]
        current_start = datetime.fromtimestamp(
            project[3]).strftime('%Y-%m-%d') if project[3] else None
        current_end = datetime.fromtimestamp(project[4]).strftime(
            '%Y-%m-%d') if project[4] else None

        print_heading(f"Editing project {self.args.code}")

        # Edit name
        while True:
            name = input(f"Project name [{current_name}]: ").strip()
            if not name:  # If empty, keep current name
                name = current_name
                break
            if name:  # If not empty, use new name
                break
            print(gray("Project name cannot be empty."))

        # Edit color
        self.show_colors()
        while True:
            color_input = input(f"Color code [{current_color}]: ").strip()
            if not color_input:  # If empty, keep current color
                color = current_color
                break
            try:
                color = int(color_input)
                if color in COLORS:
                    break
                print(gray(
                    f"Invalid color code. Please choose from: {', '.join(str(c) for c in COLORS.keys())}"))
            except ValueError:
                print(gray("Please enter a valid number."))

        # Edit start date
        while True:
            start = input(
                f"Start date (YYYY-MM-DD) [{current_start or gray('Not set')}]: ").strip()
            if not start:  # If empty, keep current start date
                start_timestamp = project[3]
                break
            start_timestamp = self.parse_date(start)
            if start_timestamp is not None:
                break

        # Edit end date
        while True:
            end = input(
                f"End date (YYYY-MM-DD) [{current_end or gray('Not set')}]: ").strip()
            if not end:  # If empty, keep current end date
                end_timestamp = project[4]
                break
            end_timestamp = self.parse_date(end)
            if end_timestamp is not None:
                break

        # Save changes
        self.db.cursor.execute('''
            UPDATE projects
            SET name = ?, color = ?, start = ?, end = ?
            WHERE code = ?
        ''', [name, color, start_timestamp, end_timestamp, self.args.code])
        self.db.commit()

        print_success(
            f'Project {name} ({self.args.code}) updated successfully')

    def remove_project(self) -> None:
        """Remove a project."""
        # First check if project exists
        project = self.db.cursor.execute('''
            SELECT code, name
            FROM projects
            WHERE code = ?
        ''', [self.args.code]).fetchall()

        if not project:
            print(gray(f'Project {self.args.code} not found.'))
            return

        project = project[0]
        name = project[1]

        # Confirm removal
        confirm = input(colorize("\nAre you sure you want to remove project "
                                 f"{name} ({self.args.code})? (y/N): ",
                                 YELLOW)).strip().lower()
        if confirm != 'y':
            print(gray('Project removal cancelled.'))
            return

        # Remove project
        self.db.cursor.execute('DELETE FROM projects WHERE code = ?',
                               [self.args.code])
        self.db.commit()

        print_success(f'Project {name} ({self.args.code}) removed '
                      'successfully')

    def show_colors(self) -> None:
        """Show available colors with preview."""
        print_heading("Available colors")
        for code, name in COLORS.items():
            color_preview = colorize(name, code)
            print(f"{code:2d}: {color_preview}")

    def save_project(self, code: str, name: str, color: int,
                     start: Optional[int], end: Optional[int]) -> None:
        """Save a new project to the database."""
        self.db.cursor.execute('''
            INSERT INTO projects (code, name, color, start, end)
            VALUES (?, ?, ?, ?, ?)
        ''', [code, name, color, start, end])
        self.db.commit()
