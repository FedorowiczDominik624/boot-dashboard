"""Boot Dashboard — entry point."""
import tkinter as tk
from datetime import date
from calendar_client import get_todays_events
from hours import load_hours, is_behind_pace
from links import open_vault, open_github, open_satellite

import traceback
from pathlib import Path

SHIP_OR_PARK = date(2026, 5, 26)


def days_until(target: date) -> int:
    """Return the number of days from today until `target` (negative if past)."""
    return (target - date.today()).days


def build_header(parent: tk.Misc) -> tk.Frame:
    """Header section: today's date + ship-or-park countdown."""
    frame = tk.Frame(parent)

    today_str = date.today().strftime("%A, %B %d, %Y")
    days = days_until(SHIP_OR_PARK)
    countdown_str = f"{days} day{'s' if days != 1 else ''} until ship-or-park"

    header_label = tk.Label(frame, text=today_str, font=("Consolas", 20))
    header_label.pack(pady=(0, 10))

    countdown_label = tk.Label(frame, text=countdown_str, font=("Consolas", 28, "bold"))
    countdown_label.pack()

    return frame

def build_today(parent: tk.Misc) -> tk.Frame:
    """Today's calendar events section: section header + one Label per event"""
    frame = tk.Frame(parent)

    today_label = tk.Label(frame, text="Today", font=("consolas", 20,))
    today_label.pack()

    events = get_todays_events()

    for event in events:
        if event["start"] == "all-day":
            text = f"all-day  {event['summary']}"
        else:
            text = f"{event['start']} – {event['end']}  {event['summary']}"
        tk.Label(frame, text=text, font=("Consolas", 14)).pack()

    return frame

def build_hours(parent: tk.Misc) -> tk.Frame:
    """Weekly hours section: Py, Pj, Fi progress with pace coloring"""

    frame = tk.Frame(parent)

    hours_label = tk.Label(frame, text="This Week", font=("Consolas", 20)).pack()

    hours = load_hours()

    days_of_week = date.today().isoweekday()

    py_logged = hours["logged"]["py"]
    py_targets = hours["targets"]["py"]
    pj_logged = hours["logged"]["pj"]
    pj_targets = hours["targets"]["pj"]
    fi_logged = hours["logged"]["fi"]
    fi_targets = hours["targets"]["fi"]

    if is_behind_pace(py_logged, py_targets, days_of_week):
        py_color = "red"
    else:
        py_color = "green"
    if is_behind_pace(pj_logged, pj_targets, days_of_week):
        pj_color = "red"
    else:
        pj_color = "green"
    if is_behind_pace(fi_logged, fi_targets, days_of_week):
        fi_color = "red"
    else:
        fi_color = "green"

    

    py_label = tk.Label(frame, text=f"Py: {hours['logged']['py']} / {hours['targets']['py']}", fg=py_color, font=("Consolas", 20)).pack()
    pj_label = tk.Label(frame, text=f"Pj: {hours['logged']['pj']} / {hours['targets']['pj']}", fg=pj_color, font=("Consolas", 20)).pack()
    fi_label = tk.Label(frame, text=f"Fi: {hours['logged']['fi']} / {hours['targets']['fi']}", fg=fi_color, font=("Consolas", 20)).pack()

    return frame

def build_buttons(parent: tk.Misc) -> tk.Frame:
    """Quick launch row: 3 buttons side by side."""
    frame = tk.Frame(parent)

    button1 = tk.Button(frame, text="Open Vault", command=open_vault)
    button2 = tk.Button(frame, text="Open GitHub", command=open_github)
    button3 = tk.Button(frame, text="Open Satellite", command=open_satellite)

    button1.pack( side="left", expand=True, fill="x")
    button2.pack( side="left", expand=True, fill="x")
    button3.pack( side="left", expand=True, fill="x")

    return frame

def main() -> None:
    try:
        root = tk.Tk()
        root.title("Boot Dashboard")
        root.geometry("900x600")

        header = build_header(root)
        header.pack(pady=40)

        today_frame = build_today(root)
        today_frame.pack(pady=20)

        hours_frame = build_hours(root)
        hours_frame.pack(pady=20)

        buttons_frame = build_buttons(root)
        buttons_frame.pack(pady=20, fill="x", padx=40)

        root.mainloop()
    except Exception:
        Path("pythonw_error.log").write_text(traceback.format_exc())
        raise

if __name__ == "__main__":
    main()
