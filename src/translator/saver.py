import os
import pandas as pd

def save_report(report: os.path, reference: os.path, translation: pd.DataFrame) -> None:

    # Build output name
    report_base = os.path.splitext(os.path.basename(report))[0]
    reference_base = os.path.splitext(os.path.basename(reference))[0]
    out_name = f"{report_base} {reference_base}.csv"
    out_path = os.path.join("out", out_name)

    # Save csv
    translation.to_csv(out_path, index=False, encoding="utf-8")
    print(f"File saved in: {out_path}")