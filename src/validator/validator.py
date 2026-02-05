import pandas as pd
from pandasgui import show

from validator.saver import save_report

def run_final_check(data: pd.DataFrame, name: str) -> pd.DataFrame:

    gui = show(data, settings={'block': True})
    corrected_df = gui.get_dataframes()[f'data']
    
    # Save button
    save_report(name=name, data=corrected_df)

    return corrected_df
