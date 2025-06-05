# ScenePlayStage.py

from ScenePlay import ScenePlay
import pygame
from Constants import *
import pyghelpers
from Baddies import BaddieMgr # BaddieMgr 임포트 확인
from Goodies import GoodieMgr # GoodieMgr 임포트 확인

class ScenePlayStage(ScenePlay):
    def __init__(self, window):
        super().__init__(window)
        self.currentStage = 1
        self.stageGoal = 20
        self.difficulty = 'normal' # 기본 난이도 설정

    def enter(self, data): # SceneMgr.goToScene에서 전달받은 데이터를 처리
        super().enter(data)
        if data is not None and 'difficulty' in data:
            self.difficulty = data['difficulty']
        
        print(f"Stage Mode: Difficulty set to {self.difficulty}")
        self.reset() # 난이도 설정 후 게임 초기화

    def reset(self):
        super().reset()
        self.currentStage = 1
        self.stageGoal = 20
        self.playingState = STATE_WAITING # STATE_PLAYING 대신 STATE_WAITING이 더 적절

        # 난이도에 따라 BaddieMgr 및 GoodieMgr 초기화
        initial_min_speed = BaddieMgr.MIN_SPEED # BaddieMgr의 기본 MIN_SPEED
        initial_max_speed = BaddieMgr.MAX_SPEED # BaddieMgr의 기본 MAX_SPEED
        initial_goodie_rate_lo = GoodieMgr.INITIAL_GOODIE_RATE_LO # GoodieMgr의 기본 값
        initial_goodie_rate_hi = GoodieMgr.INITIAL_GOODIE_RATE_HI

        if self.difficulty == 'easy':
            initial_min_speed = max(1, BaddieMgr.MIN_SPEED - 2)
            initial_max_speed = max(3, BaddieMgr.MAX_SPEED - 2)
            initial_goodie_rate_lo = GoodieMgr.INITIAL_GOODIE_RATE_LO + 10 # 굿디 더 느리게
            initial_goodie_rate_hi = GoodieMgr.INITIAL_GOODIE_RATE_HI + 10
        elif self.difficulty == 'hard':
            initial_min_speed = BaddieMgr.MIN_SPEED + 3
            initial_max_speed = BaddieMgr.MAX_SPEED + 3
            initial_goodie_rate_lo = max(10, GoodieMgr.INITIAL_GOODIE_RATE_LO - 5) # 굿디 더 빠르게
            initial_goodie_rate_hi = max(15, GoodieMgr.INITIAL_GOODIE_RATE_HI - 5)
        # 'normal'은 기본값 사용

        # BaddieMgr와 GoodieMgr를 다시 초기화 (setupGameObjects에서 이미 초기화된 경우)
        # 혹은, 이 매니저들이 난이도 매개변수를 받을 수 있도록 수정
        # 현재 코드에서는 setupGameObjects에서 BaddieMgr/GoodieMgr를 생성하므로,
        # 해당 클래스의 생성자에 난이도 관련 인자를 전달하거나,
        # reset() 메서드에서 난이도에 따라 매니저의 속성을 직접 변경해야 합니다.

        # 가장 간단한 방법은 BaddieMgr와 GoodieMgr에 난이도 설정 메서드를 추가하는 것입니다.
        self.oBaddieMgr.setDifficultySpeeds(initial_min_speed, initial_max_speed)
        self.oGoodieMgr.setInitialRates(initial_goodie_rate_lo, initial_goodie_rate_hi)


    def updateGameplay(self):
        mouseX, mouseY = pygame.mouse.get_pos()
        playerRect = self.oPlayer.update(mouseX, mouseY)
        nGoodiesHit = self.oGoodieMgr.update(playerRect)
        if nGoodiesHit > 0:
            self.score += nGoodiesHit * POINTS_FOR_GOODIE

        self.score += self.oBaddieMgr.update() * POINTS_FOR_BADDIE_EVADED
        self.scoreText.setValue(str(self.score))

        if self.oBaddieMgr.hasPlayerHitBaddie(playerRect):
            self.endGame()

        if self.score >= self.stageGoal:
            self.advanceStage()

    def advanceStage(self):
        self.currentStage += 1
        self.stageGoal += 20
        self.oBaddieMgr.increaseDifficulty(self.currentStage)
        self.oGoodieMgr.increaseFrequency(self.currentStage)
        
        self.dialogPromptText.setValue(f"Stage {self.currentStage-1} Clear! Proceed to Stage {self.currentStage}?")
        result = pyghelpers.customYesNoDialog(self.window,
                                              self.dialogPromptText,
                                              self.dialogYesButton,
                                              self.dialogNoButton)

    def endGame(self):
        pygame.mouse.set_visible(True)
        pygame.mixer.music.stop()
        self.gameOverSound.play()
        self.playingState = STATE_GAME_OVER
        # self.draw() # Ensure the game over state is drawn - 이 부분은 pyghelpers의 drawCycle에 의해 처리됨.

        dialogText = f"You reached Stage {self.currentStage} with score {self.score}. Play again?"
        self.dialogPromptText.setValue(dialogText)

        result = pyghelpers.customYesNoDialog(self.window,
                                              self.dialogPromptText,
                                              self.dialogYesButton,
                                              self.dialogNoButton)

        if result == 'Yes': # 다시 시작
            self.reset()
        else: # 하이 스코어 또는 종료
            self.goToScene(SCENE_HIGH_SCORES)