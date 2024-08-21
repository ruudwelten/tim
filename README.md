# Tim the time tracking helper

A small CLI tool to track your time written in Python.  


## Requirements

- Python 3
- [tabulate](https://pypi.org/project/tabulate/)
- [tomli](https://pypi.org/project/tomli/)


## Setup

Run this command to create the SQLite database:  

    $ ./tim.py init


## How to use

### `help`

    $ tim.py help

Show instructions on how to use Tim.  

### `new`

    $ tim.py new [-#] [-r #|--retro=#] [-t HH:MM|--time=HH:MM] [title]

Create a new timestamp with the `new` command. This saves a current timestamp
with a title. Unless an amount of minutes in the past or a specific time is
specified by the retro or time flags the current time will be used. If no title
is specified it will be empty.  
To add new timestamps to days in the past, use the numeric (`-#`) flag. Eg.
`tim.py new -2 Lorem` to add the timestamp "Lorem" for the current time to the
log of the day before yesterday.  
The numeric flag can be combined with the retro or time flags. For noon on
yesterday use: `tim.py new -1 -t 12:00`  

### `log`

    $ tim.py log [-#]

List any day's log of timestamps. By default, today's log is shown. With the
numeric (`-#`) flag the log of a day in the past can be shown.  
Eg. `tim.py log -1` for yesterday's log.  

### `group`

    $ tim.py group [-#]

With the group command you can update several timestamps' titles so that they
will be grouped together when tallying all the day's timestamps.  
With the numeric (`-#`) flag the timestamps of a day in the past can be
grouped.  

### `tally`

    $ tim.py tally [-#]

Show the tally of your day's work. All times are calculated in regard to the
next timestamp and all timestamps with the same title are tallied together.
Since the last timestamp does not have a follow up timestamp it will have a time
of zero, so make sure to add and 'End' timestamp.  
With the numeric (`-#`) flag the tally of a day in the past can be shown.  
  
### `toggle`

    $ tim.py toggle

Interactive command to toggle timestamps to be tallied or not.  

### `init`

    $ tim.py init

As explained in the _Setup_ section, the init command creates a new SQLite
database at the `db/tim.sqlite` path and initializes the database tables. If a
database is already present you get the choice to back up the database, remove
the database or quit.  


## Roadmap

- Split commands currently under the `group` command to each be a stand alone
  command
- Create a tim shell that allows different operations to be chained
- Create `edit` command to edit a specific entry
- Create `amend` command to edit latest entry
- Create command to remove entry
- Change if statement in `app.py` to registration set up to prevent this getting
  too long
- Use correct locale, now all times are UTC, which means a log past
  midnight CET is still showing the previous day
- Add projects functionality:
  - CRUD for projects (code, name, color)
  - When starting a timestamp with the project code, link it to the project and
    group in tally's, maybe even color code timestamps based on project
    eg.: `tim new ABC Started project` links "Started project" timestamp to the
    ABC project.
  - View project overview
  - Link timestamps to project manually
