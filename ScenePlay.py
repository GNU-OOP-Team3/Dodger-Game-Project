# ScenePlay.py
import pygame
from pygame.locals import *
import pygwidgets
import pyghelpers
from Player import Player
from Baddies import BaddieMgr
from Goodies import GoodieMgr
# import pygame.mixer # 사운드 제거로 인해 주석 처리 또는 제거
from Constants import (WINDOW_WIDTH, WINDOW_HEIGHT, GAME_HEIGHT,
                        BLACK, PLAYER_START_X, PLAYER_START_Y,
                        STATE_WAITING, STATE_PLAYING, STATE_PAUSED, STATE_GAME_OVER)

class ScenePlay(pyghelpers.Scene):
    def __init__(self, window):
        self.window = window
        
        # 사운드 로드 관련 코드 제거 (gameOverSound, goodieSound, backgroundMusic)

        # 플레이어 객체 생성
        self.oPlayer = Player(self.window, PLAYER_START_X, PLAYER_START_Y)
        # Baddie 관리자 객체 생성
        self.oBaddieMgr = BaddieMgr(self.window)
        # Goodie 관리자 객체 생성
        self.oGoodieMgr = GoodieMgr(self.window)
        
        self.score = 0
        self.playingState = STATE_WAITING # 초기 상태는 대기 중 (enter에서 STATE_PLAYING으로 변경)

        # UI 요소
        self.scoreText = pygwidgets.DisplayText(self.window, (WINDOW_WIDTH - 200, 10),
                                                f'Score: {self.score}', fontSize=30, textColor=BLACK,
                                                justified='right', width=190)
        
        # 사운드 버튼 및 사운드 상태 라벨 관련 코드 제거

        # 게임 오버 다이얼로그용 UI
        self.dialogPromptText = pygwidgets.DisplayText(self.window, (0, 0),
                                                    '', fontSize=30, textColor=BLACK,
                                                    justified='center', width=WINDOW_WIDTH)
        
    def getSceneKey(self):
        raise NotImplementedError("getSceneKey() 메서드는 ScenePlay의 자식 클래스에서 구현되어야 합니다.")

    def enter(self, data):
        # 씬에 진입할 때마다 호출됩니다.
        self.reset()
        pygame.mouse.set_visible(False) # 플레이어 이동이 마우스이므로 마우스 숨김
        # 배경 음악 관련 코드 제거 (pygame.mixer.music.load, play)

    def reset(self):
        # 게임 상태를 초기화합니다.
        self.score = 0
        self.scoreText.setValue(f'Score: {self.score}')
        self.oPlayer.reset() # 플레이어 위치 및 상태 초기화
        self.oBaddieMgr.reset() # Baddies 초기화
        self.oGoodieMgr.reset() # Goodies 초기화
        self.playingState = STATE_PLAYING # 게임 시작 상태로 변경
        
        # 사운드 상태 및 버튼 텍스트 초기화 관련 코드 제거
        # pygame.mixer.music.unpause() # 음악 다시 재생 관련 코드 제거

    def update(self):
        if self.playingState != STATE_PLAYING:
            return
        
        # 플레이어 업데이트는 updateGameplay에서 마우스 위치로 처리되므로, 여기서 직접 호출 필요 없음
        self.updateGameplay() # 자식 클래스에서 구현될 게임 로직

    def handleInputs(self, eventsList, keyPressedList):
        for event in eventsList:
            if event.type == QUIT:
                self.quit()

            # 사운드 버튼 처리 관련 코드 제거 (self.soundButton.handleEvent)
            
        # 플레이어 이동 입력은 마우스로 처리되므로, 키보드 입력 처리는 이 클래스에서 제거합니다.
        # if self.playingState == STATE_PLAYING:
        #     self.oPlayer.handleInputs(keyPressedList) 

    # _updateSoundState 메서드 제거

    def draw(self):
        self.window.fill(BLACK) # 배경을 검은색으로 채움
        self.oPlayer.draw()
        self.oBaddieMgr.draw()
        self.oGoodieMgr.draw()
        self.scoreText.draw()
        # 사운드 버튼 그리기 관련 코드 제거 (self.soundButton.draw)
        # 사운드 상태 라벨 그리기 관련 코드 제거 (self.soundStatusLabel.draw)

    def endGame(self):
        raise NotImplementedError("endGame() 메서드는 ScenePlay의 자식 클래스에서 구현되어야 합니다.")