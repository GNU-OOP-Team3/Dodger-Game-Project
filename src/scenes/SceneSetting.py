# High Scores scene
import pygwidgets
import pyghelpers
from src.settings.SettingData import *
from src.Constants import *

class InputNumber(pygwidgets.InputText):
    def __init__(self, window, loc, value='', fontName=None,
                 fontSize=24, width=200, textColor=BLACK,
                 backgroundColor=WHITE, focusColor=BLACK, 
                 initialFocus=False, nickName=None, callback=None,
                 mask=None, keepFocusOnSubmit=False):
        # Call the __init__ method of our base class
        super().__init__(window, loc, value, fontName, fontSize,
                         width, textColor, backgroundColor,
                         focusColor, initialFocus, nickName, callback,
                         mask, keepFocusOnSubmit)

    # Override handleEvent so we can filter for proper keys
    def handleEvent(self, event):
        if (event.type == pygame.KEYDOWN):
            # If it's not an editing or numeric key ignore it
            # Unicode value is only present on key down
            allowableKey = ((event.key in LEGAL_KEYS_TUPLE) or
                            (event.unicode in '0123456789'))
            if not allowableKey:
                return False

        # Allow the key to go through to the base class
        result = super().handleEvent(event)  
        return result

    def getValue(self):
        userString = super().getValue()
        try:
            returnValue = int(userString)
            # Ensure the value is between 0 and 100
            returnValue = max(0, min(100, returnValue))
            return returnValue
        except ValueError:
            raise ValueError('Entry is not a number, needs to have at least one digit.')

class SceneSetting(pyghelpers.Scene):
    def __init__(self, window):
        self.window = window
        self.oSettingData = SettingData()
        self.settings = self.oSettingData.getSetting()
        
        self.backgroundImage = pygwidgets.Image(self.window,
                                                (0, 0),
                                                f'{RESOURCES_PATH}/images/highScoresBackground.jpg')

        # Background Music Settings
        self.bgVolumeCaption = pygwidgets.DisplayText(window, (50, 100), 
                             f'Background Music Volume: {int(self.settings["sound"]["background"]["volume"])}',
                             fontSize=24, width=300, justified='left')
        self.bgVolumeInput = InputNumber(window, (80, 130), 
                             str(int(self.settings["sound"]["background"]["volume"])), width=50)
        self.bgMusicCheckBox = pygwidgets.TextCheckBox(self.window,
                                                   (400, 130),
                                                    "Play Background Music",
                                                    self.settings['sound']['background']['playing'],
                                                    textColor=BLACK)
        
        # Sound Effects Settings
        self.effectsVolumeCaption = pygwidgets.DisplayText(window, (50, 200), 
                             f'Sound Effects Volume: {int(self.settings["sound"]["effects"]["volume"])}',
                             fontSize=24, width=300, justified='left')
        self.effectsVolumeInput = InputNumber(window, (80, 230), 
                             str(int(self.settings["sound"]["effects"]["volume"])), width=50)
        
        qt_PATH = f"{RESOURCES_PATH}/images/quit"
        self.quitButton = pygwidgets.CustomButton(self.window,
                                                  (30, 650),
                                                  up=f'{qt_PATH}/quitNormal.png',
                                                  down=f'{qt_PATH}/quitDown.png',
                                                  over=f'{qt_PATH}/quitOver.png',
                                                  disabled=f'{qt_PATH}/quitDisabled.png')

        bk_PATH = f"{RESOURCES_PATH}/images/back"
        self.backButton = pygwidgets.CustomButton(self.window,
                                                 (240, 650),
                                                 up=f'{bk_PATH}/backNormal.png',
                                                 down=f'{bk_PATH}/backDown.png',
                                                 over=f'{bk_PATH}/backOver.png',
                                                 disabled=f'{bk_PATH}/backDisabled.png')

        rs_PATH = f"{RESOURCES_PATH}/images/reset"
        self.resetSettingButton = pygwidgets.CustomButton(self.window,
                                                 (450, 650),
                                                 up=f'{rs_PATH}/resetNormal.png',
                                                 down=f'{rs_PATH}/resetDown.png',
                                                 over=f'{rs_PATH}/resetOver.png',
                                                 disabled=f'{rs_PATH}/resetDisabled.png')

        self.showSettings()

    def getSceneKey(self):
        return SCENE_SETTING

    def reset(self):
        pass
    
    def showSettings(self):
        # Get the current settings and update UI elements
        self.settings = self.oSettingData.getSetting()
        
        # Update Background Music settings
        self.bgVolumeCaption.setValue(f'Background Music Volume: {int(self.settings["sound"]["background"]["volume"])}')
        self.bgVolumeInput.setValue(str(int(self.settings["sound"]["background"]["volume"])))
        self.bgMusicCheckBox.setValue(self.settings['sound']['background']['playing'])
        
        # Update Sound Effects settings
        self.effectsVolumeCaption.setValue(f'Sound Effects Volume: {int(self.settings["sound"]["effects"]["volume"])}')
        self.effectsVolumeInput.setValue(str(int(self.settings["sound"]["effects"]["volume"])))

    def update(self):
        pass  # No need for continuous updates

    def handleInputs(self, events, keyPressedList):
        for event in events:
            if self.quitButton.handleEvent(event):
                self.quit()

            elif self.backButton.handleEvent(event):
                self.goToScene(SCENE_PLAY)

            elif self.resetSettingButton.handleEvent(event):
                # Reset settings and update UI
                self.oSettingData.resetSetting()
                self.settings = self.oSettingData.getSetting()
                self.showSettings()

            # Handle background music volume input changes
            if self.bgVolumeInput.handleEvent(event):
                try:
                    new_volume = self.bgVolumeInput.getValue()
                    if self.updateSettings(['sound', 'background', 'volume'], new_volume):
                        self.bgVolumeCaption.setValue(f'Background Music Volume: {new_volume}')
                        print(f"Setting changed: Background volume -> {new_volume}%")
                except ValueError:
                    pass  # Ignore invalid input

            # Handle sound effects volume input changes
            if self.effectsVolumeInput.handleEvent(event):
                try:
                    new_volume = self.effectsVolumeInput.getValue()
                    if self.updateSettings(['sound', 'effects', 'volume'], new_volume):
                        self.effectsVolumeCaption.setValue(f'Sound Effects Volume: {new_volume}')
                        print(f"Setting changed: Effects volume -> {new_volume}%")
                except ValueError:
                    pass  # Ignore invalid input

            # Handle background music checkbox changes
            if self.bgMusicCheckBox.handleEvent(event):
                is_playing = self.bgMusicCheckBox.getValue()
                if self.updateSettings(['sound', 'background', 'playing'], is_playing):
                    print(f"Setting changed: Background music -> {'Playing' if is_playing else 'Paused'}")

    def draw(self):
        self.backgroundImage.draw()
        self.bgVolumeCaption.draw()
        self.bgVolumeInput.draw()
        self.bgMusicCheckBox.draw()
        self.effectsVolumeCaption.draw()
        self.effectsVolumeInput.draw()
        self.quitButton.draw()
        self.resetSettingButton.draw()
        self.backButton.draw()

    def updateSettings(self, key_path, new_value):
        """설정을 업데이트하고 UI를 갱신하는 헬퍼 메서드"""
        self.settings = self.oSettingData.getSetting()
        current = self.settings
        for key in key_path[:-1]:
            current = current[key]
        if current[key_path[-1]] != new_value:
            current[key_path[-1]] = new_value
            self.oSettingData.setSetting(self.settings)
            return True
        return False