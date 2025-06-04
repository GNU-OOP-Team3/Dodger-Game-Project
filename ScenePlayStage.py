# ScenePlayStage.py
from ScenePlay import ScenePlay
import pygame # 추가
from Constants import * # 추가
import pyghelpers

class ScenePlayStage(ScenePlay):
    def __init__(self, window):
        super().__init__(window)
        self.currentStage = 1
        self.stageGoal = 20

    def reset(self):
        super().reset()
        self.currentStage = 1
        self.stageGoal = 20
        self.playingState = STATE_PLAYING

    def updateGameplay(self):
        mouseX, mouseY = pygame.mouse.get_pos()
        playerRect = self.oPlayer.update(mouseX, mouseY)
        nGoodiesHit = self.oGoodieMgr.update(playerRect)
        if nGoodiesHit > 0:
            self.score += nGoodiesHit * POINTS_FOR_GOODIE

        self.score += self.oBaddieMgr.update() * POINTS_FOR_BADDIE_EVADED
        self.scoreText.setValue(str(self.score)) # setValue는 문자열을 받음

        if self.oBaddieMgr.hasPlayerHitBaddie(playerRect):
            self.endGame()

        if self.score >= self.stageGoal:
            self.advanceStage()

    def advanceStage(self):
        self.currentStage += 1
        self.stageGoal += 20
        # Consider increasing difficulty here
        self.oBaddieMgr.increaseDifficulty(self.currentStage)
        self.oGoodieMgr.increaseFrequency(self.currentStage)
        # self.oBaddieMgr.increaseDifficulty(self.currentStage) # 이 메서드는 BaddieMgr에 정의되어야 함
        # self.oGoodieMgr.increaseFrequency(self.currentStage) # 이 메서드는 GoodieMgr에 정의되어야 함
        
        pyghelpers.customYesNoDialog(self.window, "메시지")
        

    def endGame(self):
        pygame.mouse.set_visible(True)
        pygame.mixer.music.stop()
        self.gameOverSound.play()
        self.playingState = STATE_GAME_OVER
        self.draw() # Ensure the game over state is drawn

        dialogText = f"You reached Stage {self.currentStage} with score {self.score}"
        pyghelpers.customYesNoDialog(self.window, dialogText)

        self.newGameButton.enable()
        self.highScoresButton.enable()
        self.soundCheckBox.enable()
        self.quitButton.enable()
