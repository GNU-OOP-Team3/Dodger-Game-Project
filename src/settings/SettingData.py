from src.Constants import *
from pathlib import Path
import json

class SettingData():
    def __init__(self) -> None:
        self.DEFAULT_SETTINGS = {
            "sound": {
                "background": {
                    "volume": 59,
                    "playing": 0
                },
                "effects": {
                    "volume": 30
                }
            }
        }
        self.oFilePath = Path("src/settings/Settings.json")

        try:
            with open(self.oFilePath, 'r') as setting_data:
                self.settings = json.load(setting_data)
        except FileNotFoundError:
            self.resetSetting()
            return

    def saveSetting(self):
        with open(self.oFilePath, 'w') as f:
            json.dump(self.settings, f, indent=4)

    def resetSetting(self):
        self.settings = self.DEFAULT_SETTINGS.copy()
        self.saveSetting()

    def setSetting(self, newSettings):
        self.settings = newSettings
        self.saveSetting()

    def getSetting(self):
        with open(self.oFilePath, 'r') as setting_data:
            self.settings = json.load(setting_data)
        return self.settings