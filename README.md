# Tim the time tracking helper

A small CLI tool to track your time written in Python.  


## Requirements

- Python 3
- [tabulate](https://pypi.org/project/tabulate/)


## Setup

Run this command to create the SQLite database:  

    $ ./tim.py init


## How to use

### `help`

    $ tim.py help

Show instructions on how to use Tim.  

### `new`

    $ tim.py new [-r #|--retro=#] [title]

Create a new timestamp with the `new` command. This saves a current timestamp
with a title. Unless an amount of minutes in the past is specified by the
`-r`/`--retro` flag the current time will be used. If no title is specified it
will be empty.  

### `log`

    $ tim.py log [-#]

List any day's log of timestamps. By default, today's list is shown. With the
numbered (`-#`) flag the logs of a day in the past can be shown.  
Eg. `tim.py log -1` for yesterday's logs.  

### `group`

    $ tim.py group [-#]

With the group command you can update several timestamps' titles so that they
will be grouped together when tallying all the day's timestamps.  
With the numbered (`-#`) flag the timestamps of a day in the past can be
grouped.  

### `tally`

    $ tim.py tally [-#]

Show the tally of your day's work. All times are calculated in regard to the
next timestamp and all timestamps with the same title are tallied together.
Since the last timestamp does not have a follow up timestamp it will have a time
of zero, so make sure to add and 'End' timestamp.  
With the numbered (`-#`) flag the tally of a day in the past can be shown.  

### `init`

    $ tim.py init

As explained in the _Setup_ section, the init command creates a new SQLite
database at the `db/tim.sqlite` path and initializes the database tables. If a
database is already present you get the choice to back up the database, remove
the database or quit.  

## To do:

- Create edit command to edit a specific entry
- Create ammend command to edit latest entry
- Create command to remove entry
- Create possibilty to exclude entry from tally (end of day, lunch, etc.)
