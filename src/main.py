import os
import sys
import pandas as pd

from argparser  import argparser  as ap
from translator import fetcher    as fc
from translator import translator as tr
from translator import saver      as sv

def main():

    # Fetch reference from Google Classroom
    reference = args.reference
    classroom = fc.fetch_classroom_reference(reference=reference)
        
    os.makedirs("out", exist_ok=True)

    # Fetch report from Kahoot & translate
    reports = args.report    
    for report in reports:
        # Translate report
        total, kahoot = fc.fetch_kahoot_report(report=report)
        translation = tr.translate_report(report=kahoot, total=total, reference=classroom)
        # Save report
        sv.save_report(report=report, reference=reference, translation=translation)

    return os.EX_OK
    
if __name__ == '__main__':
    
    # parse arguments
    args = ap.parse()
    # run main script
    status = main()
    
    sys.exit(status)