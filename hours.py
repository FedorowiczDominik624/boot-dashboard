"""Hour tracker - loads hours.json from disk"""

import json
import tkinter as tk

def load_hours() -> dict:
    """Load the current week's data from hours.json"""
    with open("hours.json") as f:
        return json.load(f)
    
def is_behind_pace(logged: float, target: float, day_of_week: int) -> bool:
    """Return True if logged hours are behind expected pace for this day of the week.
    
    day_of_week uses ISO convention: Monday=1, Tuesday=2, ..., Sunday=7.
    """
    expected = target * (day_of_week / 7 )
    if logged < expected:
        return True
    else:
        return False

