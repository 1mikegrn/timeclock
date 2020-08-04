# timeclock

## A CLI tool for simple time tracking

_________________________________________

This CLI tool provides basic logging functionality for time at work. Data collected is periodically stored into a .json file until a full work instance is logged, at which point the .json data is committed to an on-disk SQLite file for storage.

The tool is initialized from the command line via the keyword `clk`. The first entry after `clk` corresponds to one of the command arguments for getting the current clock status, clocking in, clocking out, clocking on_break, clocking off_break, getting the database, and getting the break log. Each argument has a few variants which can be chosen from the list of options below:

```text
get current status: ['clk status', 'clk s']
clock in: ['clk in', 'clk n']
clock out: ['clk out', 'clk o']
go on break: ['clk on_break', 'clk +b']
go off break: ['clk off_break', 'clk -b']
get database: ['clk get_db', 'clk db']
get break log: ['clk get_logs', 'clk log', 'clk lg'] + '-id <ID>'
reset system/delete all data: ['clk RESET']
```

flagged arguments can be passed to the previous commands through `-flag arg` syntax. The available flags are provided below:

`-id <ID>` *must* be tagged to `clk get_logs` so to acquire the corresponding break log. These ID's can be found in the database under the `break_log` attribute.

`-m "<STRING>"` can be tagged to `clk in` or `clk on_break` so to add descriptive text strings to the instances. `clk in -m <STRING>` adds a string to the `task` attribute of the database, and is meant for denoting work tasks. `clk on_break -m <STRING>` adds a string to  the `notes` attribute of the break log, and is meant for denoting break activities. If flag is not provided, data entries default to `None`.

`-f <t>` can be tagged to both `clk get_db` and `clk get_logs` so to display time in specific formats (database stores epoch time but converts to an (%H:%M:%S) string for display by default). Current `<t>` options are:

```text
for epoch time: ['epoch', 'e']
```

## Installation

This tool can be installed with pip and git:

```text
pip install git+https://github.com/1mikegrn/timeclock
```
