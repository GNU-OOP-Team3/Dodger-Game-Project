# Splash scene - first scene the user sees
import pygwidgets
import pyghelpers
from src.Constants import *

class SceneSplash(pyghelpers.Scene):
    def __init__(self, window):
        self.window = window

        self.backgroundImage = pygwidgets.Image(self.window,
                                                (0, 0), f'{RESOURCES_PATH}/images/splashBackground.jpg')
        self.dodgerImage = pygwidgets.Image(self.window,
                                                (150, 30), f'{RESOURCES_PATH}/images/dodger.png')

        st_PATH = f"{RESOURCES_PATH}/images/start"
        self.startButton = pygwidgets.CustomButton(self.window, (250, 500),
                                                up=f'{st_PATH}/startNormal.png',
                                                down=f'{st_PATH}/startDown.png',
                                                over=f'{st_PATH}/startOver.png',
                                                disabled=f'{st_PATH}/startDisabled.png',
                                                enterToActivate=True)

        qt_PATH = f"{RESOURCES_PATH}/images/quit"
        self.quitButton = pygwidgets.CustomButton(self.window, (30, 650),
                                                up=f'{qt_PATH}/quitNormal.png',
                                                down=f'{qt_PATH}/quitDown.png',
                                                over=f'{qt_PATH}/quitOver.png',
                                                disabled=f'{qt_PATH}/quitDisabled.png')

        gth_PATH = f"{RESOURCES_PATH}/images/gotoHighScores"
        self.highScoresButton = pygwidgets.CustomButton(self.window, (360, 650),
                                                up=f'{gth_PATH}/gotoHighScoresNormal.png',
                                                down=f'{gth_PATH}/gotoHighScoresDown.png',
                                                over=f'{gth_PATH}/gotoHighScoresOver.png',
                                                disabled=f'{gth_PATH}/gotoHighScoresDisabled.png')

    def getSceneKey(self):
        return SCENE_SPLASH

    def handleInputs(self, events, keyPressedList):
        for event in events:
            if self.startButton.handleEvent(event):
                self.goToScene(SCENE_PLAY)
            elif self.quitButton.handleEvent(event):
                self.quit()
            elif self.highScoresButton.handleEvent(event):
                self.goToScene(SCENE_HIGH_SCORES)

    def draw(self):
        self.backgroundImage.draw()
        self.dodgerImage.draw()
        self.startButton.draw()
        self.quitButton.draw()
        self.highScoresButton.draw()
