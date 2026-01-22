import re
import pandas as pd
from os import path

from translator.config import kahoot_to_classroom

k2c = kahoot_to_classroom()

def fetch_kahoot_report(report: path) -> pd.DataFrame:
    
    # Read excel from row 1 to get total
    total = pd.read_excel(report, sheet_name=k2c.sheet_total).T
    total = total.rename(columns=total.iloc[0]).drop(total.index[0])
    total = str(total["Played"].iloc[0]).strip().split('of')[0]
    
    # Read excel from row 1 to get names
    data = pd.read_excel(report, sheet_name=k2c.sheet_name, header=k2c.header)
    
    return total, data

def fetch_classroom_reference(reference: path) -> list:
    
    # Read text file reference as list of lines
    data = [item.strip() for item in open(reference).readlines()]
    
    return data