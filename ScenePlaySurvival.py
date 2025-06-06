# ScenePlaySurvival.py

from ScenePlay import ScenePlay
from Timer import Timer
import pygame
from Constants import *
import pyghelpers

class ScenePlaySurvival(ScenePlay):
    SURVIVAL_TIME = 30 # 생존 목표 시간 (기본값)
    SCORE_PER_SECOND = 10 # 1초당 얻는 점수
    POINTS_FOR_GOODIE_SURVIVAL = 50 # 서바이벌 모드에서 Goodie 획득 시 추가 점수

    def __init__(self, window):
        super().__init__(window)
        self.survivalTimer = Timer(self.SURVIVAL_TIME, "survival", self.timerFinished)

    def reset(self):
        super().reset()
        self.survivalTimer.start()
        self.playingState = STATE_WAITING
        # 서바이벌 모드에서는 난이도 증가 로직을 초기화하지 않음 (스테이지 모드와 분리)
        # 필요하다면 BaddieMgr와 GoodieMgr의 난이도를 기본값으로 설정

    def updateGameplay(self):
        mouseX, mouseY = pygame.mouse.get_pos()
        playerRect = self.oPlayer.update(mouseX, mouseY)
        
        # Goodie 획득 시 점수 추가
        nGoodiesHit = self.oGoodieMgr.update(playerRect)
        if nGoodiesHit > 0:
            self.score += nGoodiesHit * self.POINTS_FOR_GOODIE_SURVIVAL # 서바이벌 모드 점수

        # Baddie 피할 때 점수 추가 (기존 로직 유지)
        self.score += self.oBaddieMgr.update() * POINTS_FOR_BADDIE_EVADED # POINTS_FOR_BADDIE_EVADED 사용

        # 시간 기반 점수 추가
        # 매 프레임마다 시간을 확인하여 점수를 업데이트
        # 타이머가 멈추지 않았다면 경과 시간에 비례하여 점수 증가
        if self.survivalTimer.isRunning(): # Timer 클래스에 isRunning() 메서드 추가 필요
            self.score = int(self.survivalTimer.getTime() * self.SCORE_PER_SECOND)

        self.scoreText.setValue(f'Score: {self.score}')

        if self.oBaddieMgr.hasPlayerHitBaddie(playerRect):
            self.endGame(False) # 생존 실패

        if self.survivalTimer.update(): # 타이머가 완료되면
            self.endGame(True) # 생존 성공

    def timerFinished(self, nickname):
        # 타이머가 완료되었을 때 호출되는 콜백 (현재는 비어있음)
        pass

    def endGame(self, survived):
        pygame.mouse.set_visible(True)
        pygame.mixer.music.stop()
        self.gameOverSound.play()
        self.playingState = STATE_GAME_OVER
        # self.draw() # pyghelpers의 drawCycle에 의해 처리됨.

        dialogText = f"You survived for {int(self.survivalTimer.getTime())} seconds! Your score is {self.score}. Play again?" if survived \
                     else f"You failed! Your score is {self.score}. Play again?"
        self.dialogPromptText.setValue(dialogText) # ScenePlay에서 상속받은 dialogPromptText 사용

        result = pyghelpers.customYesNoDialog(self.window,
                                              self.dialogPromptText,
                                              self.dialogYesButton,
                                              self.dialogNoButton)

        if result == 'Yes': # 다시 시작
            self.reset()
        else: # 하이 스코어 또는 종료
            self.goToScene(SCENE_HIGH_SCORES)