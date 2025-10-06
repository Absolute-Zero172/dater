import argparse as ap
from daterutils import get_files, date_files

# declare parser
parser = ap.ArgumentParser(
    prog="dater",
    description="a utility that appends the modified date to the front of file names"
)

"""
**parser flags**

-p --pattern
--format 
--delimiter 
--no-pad-delimiter
-t --titleize
--no-check-prenamed
-y --force
"""

# add arguments
parser.add_argument('-p', '--pattern', type=str, default="*.*", help='search pattern (default: *.*)')
parser.add_argument('--format', type=str, default="%Y.%m.%d", help='date format (default: yyyy.mm.dd)')
parser.add_argument('--delimiter', type=str, default="--", help='delimiter between date and filename (default: --)')
parser.add_argument('--no-pad-delimiter', action='store_false',
                    help='remove spaces on ends of default delimiter (default=false)')
parser.add_argument('-t', '--titleize', action='store_true', help='runs .title() on original titles')
parser.add_argument('--no-check-prenamed', action='store_false', help='bypasses check to guess if files\
 have already been renamed and does not pre-remove prefix')
parser.add_argument('-y', '--force', action='store_false', help='bypasses confirmation step; NOT RECOMMENDED')

# main
if __name__ == '__main__':
    # parse args
    args = parser.parse_args()

    # rename files
    files = get_files(search_pattern=args.pattern)
    date_files(
        files,
        format_string=args.format,
        delimiter=args.delimiter,
        pad_delimiter=args.no_pad_delimiter,
        titleize=args.titleize,
        ask=args.force,
        check_prenamed=args.no_check_prenamed
    )
