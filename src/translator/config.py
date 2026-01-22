from dataclasses import dataclass, field
from typing import List

@dataclass
class kahoot_to_classroom:
    sheet_total:  str = "Overview"
    sheet_name:   str = "Final Scores"
    header:       int = 2
    keep_columns: List[str] = field(
        default_factory=lambda: ["Rank", "Player", "Total Score (points)"]
    )