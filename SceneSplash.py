# SceneSplash.py
import pygame
import pygwidgets
import pyghelpers
from Constants import (WINDOW_WIDTH, WINDOW_HEIGHT, BLACK, WHITE, FONT_NAME,
                        SCENE_PLAY_STAGE, SCENE_PLAY_SURVIVAL, SCENE_HIGH_SCORES, # K_ 제거
                        DIFFICULTY_EASY, DIFFICULTY_NORMAL, DIFFICULTY_HARD) # 난이도 상수 임포트

class SceneSplash(pyghelpers.Scene):
    def __init__(self, window):
        self.window = window

        # 제목 텍스트
        self.titleText = pygwidgets.DisplayText(self.window, (0, 100), 'Dodger Game',
                                               fontSize=80, textColor=WHITE, justified='center', width=WINDOW_WIDTH)
        
        # 버튼들
        # 난이도 버튼
        self.easyButton = pygwidgets.TextButton(self.window, (300, 250), 'Easy', width=200, height=50)
        self.normalButton = pygwidgets.TextButton(self.window, (300, 310), 'Normal', width=200, height=50)
        self.hardButton = pygwidgets.TextButton(self.window, (300, 370), 'Hard', width=200, height=50)

        # 모드 선택 버튼
        self.survivalModeButton = pygwidgets.TextButton(self.window, (300, 430), 'Survival Mode', width=200, height=50)
        self.highScoresButton = pygwidgets.TextButton(self.window, (300, 490), 'High Scores', width=200, height=50)
        self.quitButton = pygwidgets.TextButton(self.window, (300, 550), 'Quit', width=200, height=50)

    def getSceneKey(self):
        return 'splash' # Constants.SCENE_SPLASH와 동일한 문자열

    def handleInputs(self, eventsList, keyPressedList):
        for event in eventsList:
            if event.type == pygame.QUIT:
                self.quit()

            # 난이도 버튼 클릭 처리 (스테이지 모드)
            if self.easyButton.handleEvent(event):
                self.goToScene(SCENE_PLAY_STAGE, {'difficulty': DIFFICULTY_EASY})
            elif self.normalButton.handleEvent(event):
                self.goToScene(SCENE_PLAY_STAGE, {'difficulty': DIFFICULTY_NORMAL})
            elif self.hardButton.handleEvent(event):
                self.goToScene(SCENE_PLAY_STAGE, {'difficulty': DIFFICULTY_HARD})
            
            # 서바이벌 모드 버튼 클릭 처리
            elif self.survivalModeButton.handleEvent(event):
                self.goToScene(SCENE_PLAY_SURVIVAL) # 서바이벌 모드는 난이도 선택 없이 바로 시작

            # 최고 점수 버튼 클릭 처리
            elif self.highScoresButton.handleEvent(event):
                self.goToScene(SCENE_HIGH_SCORES)
            
            # 종료 버튼 클릭 처리
            elif self.quitButton.handleEvent(event):
                self.quit()

    def draw(self):
        self.window.fill(BLACK) # 배경색 채우기
        self.titleText.draw()
        self.easyButton.draw()
        self.normalButton.draw()
        self.hardButton.draw()
        self.survivalModeButton.draw()
        self.highScoresButton.draw()
        self.quitButton.draw()

    # enter/leave, update 메서드는 이 씬에서는 필요 없으므로 생략