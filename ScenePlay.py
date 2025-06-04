# ScenePlay.py
from pygame.locals import *
import pygwidgets
import pyghelpers
from Player import Player
from Baddies import BaddieMgr
from Goodies import GoodieMgr
from Constants import * # Constants import 추가
import pygame # pygame import 추가

class ScenePlay(pyghelpers.Scene):

    def __init__(self, window):
        self.window = window
        self.setupUI()
        self.setupGameObjects()

        self.score = 0
        self.playingState = STATE_WAITING # Constants에 정의된 STATE_WAITING 사용

    def setupUI(self):
        # UI 요소 초기화 (Constants 값 사용)
        self.scoreText = pygwidgets.DisplayText(self.window, (WINDOW_WIDTH - 150, 10),
                                                'Score: 0', fontSize=30, textColor=WHITE)
        self.newGameButton = pygwidgets.CustomButton(self.window, (250, 500),
                                                up='images/startNormal.png',
                                                down='images/startDown.png',
                                                over='images/startOver.png',
                                                disabled='images/startDisabled.png')
        self.highScoresButton = pygwidgets.CustomButton(self.window, (360, 650),
                                                up='images/gotoHighScoresNormal.png',
                                                down='images/gotoHighScoresDown.png',
                                                over='images/gotoHighScoresOver.png',
                                                disabled='images/gotoHighScoresDisabled.png')
        self.soundCheckBox = pygwidgets.CustomCheckBox(self.window, (10, 10),
                                                     value=True,
                                                     on='images/checkBoxOn.png',
                                                     off='images/checkBoxOff.png')
        self.soundText = pygwidgets.DisplayText(self.window, (40, 10), 'Sound On', fontSize=24, textColor=WHITE)

        self.quitButton = pygwidgets.CustomButton(self.window, (30, 650),
                                                up='images/quitNormal.png',
                                                down='images/quitDown.png',
                                                over='images/quitOver.png',
                                                disabled='images/quitDisabled.png')

        # 사운드 로드 (경로가 올바른지 확인)
        pygame.mixer.music.load('sounds/background.mp3')
        self.gameOverSound = pygame.mixer.Sound('sounds/gameOver.wav')


    def setupGameObjects(self):
        self.oPlayer = Player(self.window)
        self.oBaddieMgr = BaddieMgr(self.window)
        self.oGoodieMgr = GoodieMgr(self.window)

    def reset(self):
        self.score = 0
        self.scoreText.setValue('Score: ' + str(self.score)) # setValue는 문자열을 받음
        self.oBaddieMgr.reset()
        self.oGoodieMgr.reset()
        pygame.mixer.music.play(-1, 0.0) # Reset 시 음악 재생 시작

    def getSceneKey(self):
        return SCENE_PLAY # 상수 SCENE_PLAY 사용

    def enter(self, data):
        self.reset() # 씬 진입 시 게임 리셋
        pygame.mouse.set_visible(False) # 게임 플레이 중 마우스 숨기기
        # 게임 시작 시 버튼 비활성화 (ScenePlay에서 실제 게임이 시작되기 전까지)
        self.newGameButton.disable()
        self.highScoresButton.disable()
        self.soundCheckBox.disable()
        self.quitButton.disable()
        pygame.mixer.music.play(-1, 0.0) # 씬 진입 시 음악 재생 시작


    def handleInputs(self, events, keyPressedList):
        # inputs 처리 로직 추가
        for event in events:
            if self.newGameButton.handleEvent(event):
                self.reset()
                self.playingState = STATE_PLAYING
                pygame.mouse.set_visible(False)
                pygame.mixer.music.play(-1, 0.0)
                self.newGameButton.disable()
                self.highScoresButton.disable()
                self.soundCheckBox.disable()
                self.quitButton.disable()

            elif self.highScoresButton.handleEvent(event):
                self.goToScene(SCENE_HIGH_SCORES)
            elif self.soundCheckBox.handleEvent(event):
                if self.soundCheckBox.getValue():
                    pygame.mixer.music.set_volume(1.0)
                else:
                    pygame.mixer.music.set_volume(0.0)
            elif self.quitButton.handleEvent(event):
                self.quit()

    def update(self):
        if self.playingState != STATE_PLAYING:
            return
        self.updateGameplay()

    def updateGameplay(self):
        # 이 메서드는 ScenePlayStage 또는 ScenePlaySurvival에서 오버라이드 됨
        raise NotImplementedError("이 메서드는 자식 클래스에서 override 해야 합니다.")

    def draw(self):
        # 화면 그리기 로직 추가
        self.window.fill(BLACK) # 배경색 채우기 (Constants에 BLACK 정의)
        self.oPlayer.draw()
        self.oBaddieMgr.draw()
        self.oGoodieMgr.draw()
        self.scoreText.draw()
        if self.playingState == STATE_GAME_OVER:
            # 게임 오버 시 버튼들 그리기
            self.newGameButton.draw()
            self.highScoresButton.draw()
            self.soundCheckBox.draw()
            self.quitButton.draw()