Dater
=================================

Dater is a file dating utility that appends the modified date to the beginning of a file name in order to allow for more
convenient sorting and file lookup.

### Features ###

- Easy to read rich terminal output
- Simple to use interface
- Automatic date retrieval
- ISO1801 default compliance
- Customizable

## How to Use ##

### Terminal Flags/Options ###

- `--help` - shows help text and exits
- `-p` or `--pattern` - outlines the search pattern for which files to rename
  - `-p *.*` - All files in current directory (defualt)
  - `-p <directory>\*.*` - All files in a different relative directory
  - `-p *.py` - Only rename .py files in current directory
- `--format` - custom date format using [standard date format codes](https://docs.python.org/3.12/library/datetime.html#strftime-strptime-behavior)
  - `--format "%Y.%m.%d"` - yyyy-mm-dd (default)
- `--delimiter` - custom delimiter between date and file name
  - `--delimiter "--"` - "--" default
- `--no-pad-delimiter` - if used, this flag removes the additional spaces placed on either side of the delimiter
- `t` or `--titlelize` - uses str.title() on the original file name
- `-y` or `--force` - skips file renaming confirmation step; this flag is generally not recommended

