import os
import sys
import pandas as pd
import json

from argparser  import argparser  as ap
from cfgparser  import cfgparser  as cp
from cfgparser.config import kahoot_to_classroom

from translator import fetcher    as fc
from translator import translator as tr
from translator import saver      as sv

from gui import AppGUI    
    
cp_cfg = kahoot_to_classroom()

def main():
    
    # Parse CLI arguments
    args = ap.parse()

    if args.config:
        # Load configuration from .ini
        config = cp.load_config(args.config)

    # Ensure output directory exists
    os.makedirs("out", exist_ok=True)

    with open("src/interface/settings.json", "r", encoding="utf-8") as f:
        settings = json.load(f)

    with open("src/interface/template.json", "r", encoding="utf-8") as f:
        template = json.load(f)
        
    app = AppGUI(settings=settings, template=template)
    app.mainloop()
    return os.EX_OK
    
if __name__ == '__main__':
    # run main script
    status = main()
    # exit with return status
    sys.exit(status)