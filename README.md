# Boot Dashboard

A Python desktop dashboard that auto-launches on Windows boot. Built as a Python learning project + personal accountability tool.

Punches me in the face every morning with:
- This week's Python / Project / Financial hour progress vs. weekly targets
- Days until Month 1 deployment-goal checkpoint
- Today's Google Calendar events
- Quick-launch buttons to my Obsidian vault, GitHub, and Satellite Orbit Predictor repo

**Status:** WIP — v1 MVP in progress. Hard deadline: May 24, 2026. Ship or park.

---

## Quick start (once shipped)

```powershell
git clone https://github.com/FedorowiczDominik624/boot-dashboard.git
cd boot-dashboard
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
python main.py
```

You'll also need a `credentials.json` from Google Cloud Console for calendar integration. See setup section (TBD post-Phase 4).

---

## Project plan

Full spec lives in the project vault:
- `(C) MVP Spec.md` — acceptance criteria, wireframe, hours.json schema
- `(C) Roadmap.md` — phase-by-phase build manual (Phase 0 → Phase 5)

License: MIT (matches Satellite Orbit Predictor repo convention).
