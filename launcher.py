"""Outer launcher — wraps main.py import + call in try/except to catch import-time errors."""
import traceback
from pathlib import Path

try:
    from main import main
    main()
except Exception:
    Path("pythonw_error.log").write_text(traceback.format_exc())
    raise
