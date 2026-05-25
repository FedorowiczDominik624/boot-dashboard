"""Quick-launch actions for the dashboard buttons"""

import os
import webbrowser

VAULT_PATH = r"C:\Users\domin\Vaults\Dominiks-AI-Brain"
GITHUB_URL = "https://github.com/FedorowiczDominik624"
SATELLITE_URL = "https://github.com/FedorowiczDominik624/Satellite-Orbit-Predictor-Anomaly-Detector"

def open_vault() -> None:
    """Open the Obsidian vault folder in Explorer."""
    os.startfile(VAULT_PATH)

def open_github() -> None:
    """Open the GitHub profile in default browser."""
    webbrowser.open(GITHUB_URL)

def open_satellite() -> None:
    """Open the Satellite Orbit Predictor repo in default browser."""
    webbrowser.open(SATELLITE_URL)