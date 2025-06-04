# ScenePlaySurvival.py
from ScenePlay import ScenePlay
from Timer import Timer
import pygame # 추가
from Constants import * # 추가
import pyghelpers # 추가

class ScenePlaySurvival(ScenePlay):
    SURVIVAL_TIME = 30

    def __init__(self, window):
        super().__init__(window)
        self.survivalTimer = Timer(self.SURVIVAL_TIME, "survival", self.timerFinished)

    def reset(self):
        super().reset()
        self.survivalTimer.start()
        self.playingState = STATE_PLAYING

    def updateGameplay(self):
        mouseX, mouseY = pygame.mouse.get_pos()
        playerRect = self.oPlayer.update(mouseX, mouseY)
        self.oGoodieMgr.update(playerRect)
        self.oBaddieMgr.update()
        self.scoreText.setValue(str(self.score)) # setValue는 문자열을 받음

        if self.oBaddieMgr.hasPlayerHitBaddie(playerRect):
            self.endGame(False)

        if self.survivalTimer.update():
            self.endGame(True)

    def timerFinished(self, nickname):
        pass

    def endGame(self, survived):
        pygame.mouse.set_visible(True)
        pygame.mixer.music.stop()
        self.gameOverSound.play()
        self.playingState = STATE_GAME_OVER
        self.draw() # Ensure the game over state is drawn

        dialogText = f"You survived!" if survived else "You failed!"
        pyghelpers.customYesNoDialog(self.window, dialogText)

        self.newGameButton.enable()
        self.highScoresButton.enable()
        self.soundCheckBox.enable()
        self.quitButton.enable()