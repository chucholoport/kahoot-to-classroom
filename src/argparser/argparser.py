import os
import sys
from argparse import ArgumentParser, Namespace

from argparser.config import kahoot_to_classroom as k2c

def parse() -> Namespace:
    
    # Set description of argument parser
    ap = ArgumentParser(description=k2c.description, epilog=k2c.epilog)
    
    # Set arguments
    ap.add_argument('-r', '--report', nargs='*', type=str, help=k2c.report, required=True)
    ap.add_argument('-f', '--reference', type=str, help=k2c.reference, required=True)
    
    # Parse arguments
    args = ap.parse_args()
    
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

    if args.reference:
        # Validate if input file exists
        if not os.path.exists(args.reference):
            sys.stderr.write(f"error: file not found: {args.reference}\n")
            sys.exit(os.EX_NOINPUT)

        # Validate if input file format is .txt
        if not args.reference.lower().endswith(".txt"):
            sys.stderr.write(f"error: file is not .xlsx: {args.reference}\n")
            sys.exit(os.EX_DATAERR)

    return args