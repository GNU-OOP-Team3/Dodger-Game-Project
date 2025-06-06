# SceneSplash.py

import pygwidgets
import pyghelpers
from Constants import *

class SceneSplash(pyghelpers.Scene):
    def __init__(self, window):
        self.window = window

        self.backgroundImage = pygwidgets.Image(self.window, (0, 0), 'images/splashBackground.jpg')
        self.dodgerImage = pygwidgets.Image(self.window, (150, 30), 'images/dodger.png')
        
        # 난이도 선택 버튼들 (처음엔 숨김)
        self.easyButton = pygwidgets.CustomButton(self.window, (250, 400),
                                                    up='images/easyNormal.png',
                                                    down='images/easyDown.png',
                                                    over='images/easyOver.png')
        if hasattr(self.easyButton, 'setText'): self.easyButton.setText('Easy')
        self.easyButton.hide()

        self.normalButton = pygwidgets.CustomButton(self.window, (250, 470),
                                                    up='images/normalNormal.png',
                                                    down='images/normalDown.png',
                                                    over='images/normalOver.png')
        if hasattr(self.normalButton, 'setText'): self.normalButton.setText('Normal')
        self.normalButton.hide()

        self.hardButton = pygwidgets.CustomButton(self.window, (250, 540),
                                                   up='images/hardNormal.png',
                                                   down='images/hardDown.png',
                                                   over='images/hardOver.png')
        if hasattr(self.hardButton, 'setText'): self.hardButton.setText('Hard')
        self.hardButton.hide()

        # 메인 모드 선택 버튼
        self.stageModeButton = pygwidgets.CustomButton(self.window, (250, 400),
                                                up='images/startNormal.png',
                                                down='images/startDown.png',
                                                over='images/startOver.png',
                                                disabled='images/startDisabled.png',
                                                enterToActivate=True)
        if hasattr(self.stageModeButton, 'setText'): self.stageModeButton.setText('Stage Mode')

        self.survivalModeButton = pygwidgets.CustomButton(self.window, (250, 500),
                                                up='images/startNormal.png',
                                                down='images/startDown.png',
                                                over='images/startOver.png',
                                                disabled='images/startDisabled.png')
        if hasattr(self.survivalModeButton, 'setText'): self.survivalModeButton.setText('Survival Mode')

        self.highScoresButton = pygwidgets.CustomButton(self.window, (360, 650),
                                                up='images/gotoHighScoresNormal.png',
                                                down='images/gotoHighScoresDown.png',
                                                over='images/gotoHighScoresOver.png',
                                                disabled='images/gotoHighScoresDisabled.png')

        self.quitButton = pygwidgets.CustomButton(self.window, (30, 650),
                                                up='images/quitNormal.png',
                                                down='images/quitDown.png',
                                                over='images/quitOver.png',
                                                disabled='images/quitDisabled.png')

        # 현재 모드 (메인 메뉴, 스테이지 난이도 선택 등)
        self.currentScreen = 'main_menu' # 'main_menu', 'stage_difficulty_select'

    def getSceneKey(self):
        return SCENE_SPLASH

    def handleInputs(self, events, keyPressedList):
        for event in events:
            if self.currentScreen == 'main_menu':
                if self.stageModeButton.handleEvent(event):
                    self.currentScreen = 'stage_difficulty_select'
                    self.stageModeButton.hide()
                    self.survivalModeButton.hide()
                    self.highScoresButton.hide() # 난이도 선택 시 다른 버튼 숨기기
                    self.quitButton.hide()       # 난이도 선택 시 다른 버튼 숨기기
                    self.easyButton.show()
                    self.normalButton.show()
                    self.hardButton.show()

                elif self.survivalModeButton.handleEvent(event):
                    # 서바이벌 모드 시작 시 ScenePlaySurvival로 전환
                    self.goToScene(SCENE_PLAY_SURVIVAL)
                
                elif self.highScoresButton.handleEvent(event):
                    self.goToScene(SCENE_HIGH_SCORES)
                elif self.quitButton.handleEvent(event):
                    self.quit()

            elif self.currentScreen == 'stage_difficulty_select':
                if self.easyButton.handleEvent(event):
                    # 'easy' 난이도로 ScenePlayStage 시작
                    self.goToScene(SCENE_PLAY_STAGE, {'difficulty': 'easy'})
                elif self.normalButton.handleEvent(event):
                    # 'normal' 난이도로 ScenePlayStage 시작
                    self.goToScene(SCENE_PLAY_STAGE, {'difficulty': 'normal'})
                elif self.hardButton.handleEvent(event):
                    # 'hard' 난이도로 ScenePlayStage 시작
                    self.goToScene(SCENE_PLAY_STAGE, {'difficulty': 'hard'})

    def draw(self):
        self.backgroundImage.draw()
        self.dodgerImage.draw()
        
        if self.currentScreen == 'main_menu':
            self.stageModeButton.draw()
            self.survivalModeButton.draw()
            self.highScoresButton.draw()
            self.quitButton.draw()
        elif self.currentScreen == 'stage_difficulty_select':
            self.easyButton.draw()
            self.normalButton.draw()
            self.hardButton.draw()