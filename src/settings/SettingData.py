from src.Constants import *
from pathlib import Path
import json

class SettingData():
    def __init__(self) -> None:
        self.DEFAULT_SETTINGS = {
            "background": {
                "volume": 5,
                "isMute": False
            },
            "username": "Anomaly"
        }
        self.oFilePath = Path("src/settings/Settings.json")

        try:
            setting_data = self.oFilePath.read_text()
        except FileNotFoundError:
            return