import os
import pandas as pd

def save_report(name: os.path, data: pd.DataFrame) -> None:

    # Build output name
    out_name = f"{name}.csv"
    out_path = os.path.join("out", out_name)

    # Save csv
    data.to_csv(out_path, index=False, encoding="utf-8")
    print(f"Validated file saved in: {out_path}")