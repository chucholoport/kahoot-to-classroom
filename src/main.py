import os
import sys
import pandas as pd

from argparser  import argparser  as ap
from cfgparser  import cfgparser  as cp
from cfgparser.config import kahoot_to_classroom

from translator import fetcher    as fc
from translator import translator as tr
from translator import saver      as sv

cp_cfg = kahoot_to_classroom()

def main():
    
    # Parse CLI arguments
    args = ap.parse()
    # Load configuration from .ini
    config = cp.load_config(args.config)
    # Ensure output directory exists
    os.makedirs("out", exist_ok=True)

    if args.autograde:
        
        # Placeholder for Google Classroom API integration
        print("Hello World - Autograde mode enabled")
    
    else:
        
        # Fetch reference from Google Classroom
        reference = config[cp_cfg.student_list_key]
        classroom = fc.fetch_classroom_reference(reference=reference)

        # Fetch report from Kahoot & translate
        if args.report:
            for report in args.report:
                # Translate report
                total, kahoot = fc.fetch_kahoot_report(report=report)
                translation = tr.translate_report(report=kahoot, total=total, reference=classroom)
                # Save report
                sv.save_report(report=report, reference=reference, translation=translation)

        print("Manual mode completed successfully")

    return os.EX_OK
    
if __name__ == '__main__':
    # run main script
    status = main()
    # exit with return status
    sys.exit(status)