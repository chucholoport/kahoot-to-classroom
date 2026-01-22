import os
import sys
from argparse import ArgumentParser, Namespace

from argparser.config import kahoot_to_classroom as k2c

def parse() -> Namespace:
    
    # Set description of argument parser
    ap = ArgumentParser(description=k2c.description, epilog=k2c.epilog)
    
    # Set arguments
    ap.add_argument('-c', '--config', type=str, help=k2c.config, required=False)
    ap.add_argument('-r', '--report', nargs='*', type=str, help=k2c.report, required=False)
    ap.add_argument('-a', '--autograde', action="store_true", help=k2c.autograde, required=False)

    # Parse arguments
    args = ap.parse_args()
    
    if args.config:
        # Validate if input file exists
        if not os.path.exists(args.config):
            sys.stderr.write(f"error: config file not found: {args.config}\n")
            sys.exit(os.EX_NOINPUT)
        # Validate if input file format is .ini
        if not args.config.lower().endswith(".ini"):
            sys.stderr.write(f"error: config file must be .ini: {args.config}\n")
            sys.exit(os.EX_DATAERR)

    if args.report:
        for report in args.report:
            # Validate if input file exists
            if not os.path.exists(report):
                sys.stderr.write(f"error: file not found: {report}\n")
                sys.exit(os.EX_NOINPUT)
            # Validate if input file format is .xlsx
            if not report.lower().endswith(".xlsx"):
                sys.stderr.write(f"error: file is not .xlsx: {report}\n")
                sys.exit(os.EX_DATAERR)

    return args