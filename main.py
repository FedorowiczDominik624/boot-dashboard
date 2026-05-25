"""Boot Dashboard — entry point."""
import tkinter as tk
from datetime import date
from calendar_client import get_todays_events

SHIP_OR_PARK = date(2026, 5, 26)


def days_until(target: date) -> int:
    """Return the number of days from today until `target` (negative if past)."""
    return (target - date.today()).days


def build_header(parent: tk.Misc) -> tk.Frame:
    """Header section: today's date + ship-or-park countdown."""
    frame = tk.Frame(parent)

    today_str = date.today().strftime("%A, %B %d, %Y")
    countdown_str = f"{days_until(SHIP_OR_PARK)} days until ship-or-park"

    date_label = tk.Label(frame, text=today_str, font=("Consolas", 20))
    date_label.pack(pady=(0, 10))

    countdown_label = tk.Label(frame, text=countdown_str, font=("Consolas", 28, "bold"))
    countdown_label.pack()

    return frame

def build_today(parent: tk.Misc) -> tk.Frame:
    """Today's calendar events section: section header + one Label per event"""
    frame = tk.Frame(parent)
    date_label = tk.Label(frame, text="Today", font=("consolas", 20,))
    date_label.pack()
    events = get_todays_events()
    for event in events:
        tk.Label(frame, text=event["summary"], font=("Consolas", 14)).pack()
    return frame

def main() -> None:
    root = tk.Tk()
    root.title("Boot Dashboard")
    root.geometry("900x600")

    header = build_header(root)
    header.pack(pady=40)
    today_frame = build_today(root)
    today_frame.pack(pady=20)

    root.mainloop()

if __name__ == "__main__":
    main()
