#ScenePlay
from pygame.locals import *
import pygwidgets
import pyghelpers
from Player import *
from Baddies import *
from Goodies import *
from PowerUps import Score2X, SlowMotion, Invincibility
import random

BOTTOM_RECT = (0, GAME_HEIGHT + 1, WINDOW_WIDTH, WINDOW_HEIGHT - GAME_HEIGHT)
STATE_WAITING = 'waiting'
STATE_PLAYING = 'playing'
STATE_GAME_OVER = 'game over'

def showCustomYesNoDialog(theWindow, theText):
    oDialogBackground = pygwidgets.Image(theWindow, (40, 250), 'images/dialog.png')
    oPromptDisplayText = pygwidgets.DisplayText(theWindow, (0, 290),
                                        theText, width=WINDOW_WIDTH,
                                        justified='center', fontSize=36)

    oYesButton = pygwidgets.CustomButton(theWindow, (320, 370),
                                        'images/gotoHighScoresNormal.png',
                                        over='images/gotoHighScoresOver.png',
                                        down='images/gotoHighScoresDown.png',
                                        disabled='images/gotoHighScoresDisabled.png')

    oNoButton = pygwidgets.CustomButton(theWindow, (62, 370),
                                        'images/noThanksNormal.png',
                                        over='images/noThanksOver.png',
                                        down='images/noThanksDown.png',
                                        disabled='images/noThanksDisabled.png')

    choiceAsBoolean = pyghelpers.customYesNoDialog(theWindow,
                                        oDialogBackground, oPromptDisplayText,
                                        oYesButton, oNoButton)
    return choiceAsBoolean


# 추가: 파워업 매니저
class PowerUpMgr():
    POWERUP_RATE_LO = 90
    POWERUP_RATE_HI = 120

    def __init__(self, window):
        self.window = window
        self.reset()

    def reset(self):
        self.powerUps = []
        self.nFramesTilNext = PowerUpMgr.POWERUP_RATE_HI

    def update(self, thePlayerRect, scenePlay):
        collected = 0
        powerUpsCopy = self.powerUps.copy()
        for item in powerUpsCopy:
            deleteMe = item.update()
            if deleteMe:
                self.powerUps.remove(item)
            elif item.collide(thePlayerRect):
                item.apply_effect(scenePlay)  # 모든 효과 내부에서 처리
                scenePlay.dingSound.play()
                self.powerUps.remove(item)
                collected += 1


        self.nFramesTilNext -= 1
        if self.nFramesTilNext <= 0:
            self.nFramesTilNext = random.randint(self.POWERUP_RATE_LO, self.POWERUP_RATE_HI)
            choice = random.choices(
                [Goodie, Score2X, SlowMotion, Invincibility],
                weights=[0.4, 0.25, 0.25, 0.1]
            )[0]
            newItem = choice(self.window)
            self.powerUps.append(newItem)

        return collected

    def draw(self):
        for item in self.powerUps:
            item.draw()

# ----------------------
class ScenePlay(pyghelpers.Scene):

    def __init__(self, window):
        self.window = window
        self.controlsBackground = pygwidgets.Image(self.window, (0, GAME_HEIGHT), 'images/controlsBackground.jpg')
        self.quitButton = pygwidgets.CustomButton(self.window, (30, GAME_HEIGHT + 90), 'images/quitNormal.png', down='images/quitDown.png', over='images/quitOver.png', disabled='images/quitDisabled.png')
        self.highScoresButton = pygwidgets.CustomButton(self.window, (190, GAME_HEIGHT + 90), 'images/gotoHighScoresNormal.png', down='images/gotoHighScoresDown.png', over='images/gotoHighScoresOver.png', disabled='images/gotoHighScoresDisabled.png')
        self.newGameButton = pygwidgets.CustomButton(self.window, (450, GAME_HEIGHT + 90), 'images/startNewNormal.png', down='images/startNewDown.png', over='images/startNewOver.png', disabled='images/startNewDisabled.png', enterToActivate=True)
        self.soundCheckBox = pygwidgets.TextCheckBox(self.window, (430, GAME_HEIGHT + 17), 'Background music', True, textColor=WHITE)
        self.gameOverImage = pygwidgets.Image(self.window, (140, 180), 'images/gameOver.png')
        self.titleText = pygwidgets.DisplayText(self.window, (70, GAME_HEIGHT + 17), 'Score:                                 High Score:', fontSize=24, textColor=WHITE)
        self.scoreText = pygwidgets.DisplayText(self.window, (80, GAME_HEIGHT + 47), '0', fontSize=36, textColor=WHITE, justified='right')
        self.highScoreText = pygwidgets.DisplayText(self.window, (270, GAME_HEIGHT + 47), '', fontSize=36, textColor=WHITE, justified='right')

        pygame.mixer.music.load('sounds/background.mid')
        self.dingSound = pygame.mixer.Sound('sounds/ding.wav')
        self.gameOverSound = pygame.mixer.Sound('sounds/gameover.wav')

        self.oPlayer = Player(self.window)
        self.oBaddieMgr = BaddieMgr(self.window)
        self.oGoodieMgr = GoodieMgr(self.window)  # 유지됨
        self.oPowerUpMgr = PowerUpMgr(self.window)  # 추가됨

        self.highestHighScore = 0
        self.lowestHighScore = 0
        self.backgroundMusic = True
        self.score = 0
        self.scoreMultiplier = 1
        self.invincible = False
        self.slowFactor = 1.0
        self.activeTimers = []
        self.playingState = STATE_WAITING

    def getSceneKey(self):
        return SCENE_PLAY

    def enter(self, data):
        self.getHiAndLowScores()

    def getHiAndLowScores(self):
        infoDict = self.request(SCENE_HIGH_SCORES, HIGH_SCORES_DATA)
        self.highestHighScore = infoDict['highest']
        self.highScoreText.setValue(self.highestHighScore)
        self.lowestHighScore = infoDict['lowest']

    def reset(self):
        self.score = 0
        self.scoreText.setValue(self.score)
        self.getHiAndLowScores()
        self.oBaddieMgr.reset()
        self.oGoodieMgr.reset()
        self.oPowerUpMgr.reset()  # 추가됨

        self.scoreMultiplier = 1
        self.invincible = False
        self.slowFactor = 1.0
        self.activeTimers = []

        if self.backgroundMusic:
            pygame.mixer.music.play(-1, 0.0)
        self.newGameButton.disable()
        self.highScoresButton.disable()
        self.soundCheckBox.disable()
        self.quitButton.disable()
        pygame.mouse.set_visible(False)

    def handleInputs(self, eventsList, keyPressedList):
        if self.playingState == STATE_PLAYING:
            return
        for event in eventsList:
            if self.newGameButton.handleEvent(event):
                self.reset()
                self.playingState = STATE_PLAYING
            if self.highScoresButton.handleEvent(event):
                self.goToScene(SCENE_HIGH_SCORES)
            if self.soundCheckBox.handleEvent(event):
                self.backgroundMusic = self.soundCheckBox.getValue()
            if self.quitButton.handleEvent(event):
                self.quit()

    def update(self):
        # 타이머 처리
        self.activeTimers = [(key, frames - 1) for key, frames in self.activeTimers]
        expired = [key for key, frames in self.activeTimers if frames <= 0]
        self.activeTimers = [(key, frames) for key, frames in self.activeTimers if frames > 0]

        if 'scoreMultiplier' in expired:
            self.scoreMultiplier = 1
        if 'invincible' in expired:
            self.invincible = False
        if 'slow' in expired:
            self.slowFactor = 1.0


        if self.playingState != STATE_PLAYING:
            return

        mouseX, mouseY = pygame.mouse.get_pos()
        playerRect = self.oPlayer.update(mouseX, mouseY)

        # Goodies (기존 기능)
        nGoodiesHit = self.oGoodieMgr.update(playerRect)
        if nGoodiesHit > 0:
            self.dingSound.play()
            self.score += nGoodiesHit * POINTS_FOR_GOODIE * self.scoreMultiplier

        # PowerUps (추가 기능)
        self.oPowerUpMgr.update(playerRect, self)

        # Baddies
        scale = 0.0 if self.slowFactor == 0 else 1.0
        nBaddiesEvaded = self.oBaddieMgr.update(scale)
        self.score += nBaddiesEvaded * POINTS_FOR_BADDIE_EVADED
        self.scoreText.setValue(self.score)

        # 타이머 처리
        self.activeTimers = [(key, frames - 1) for key, frames in self.activeTimers]
        expired = [key for key, frames in self.activeTimers if frames <= 0]
        self.activeTimers = [(key, frames) for key, frames in self.activeTimers if frames > 0]
        if 'scoreMultiplier' in expired:
            self.scoreMultiplier = 1
        if 'invincible' in expired:
            self.invincible = False
        if 'slow' in expired:
            self.slowFactor = 1.0

        # 충돌 체크
        if not self.invincible and self.oBaddieMgr.hasPlayerHitBaddie(playerRect):
            pygame.mouse.set_visible(True)
            pygame.mixer.music.stop()
            self.gameOverSound.play()
            self.playingState = STATE_GAME_OVER
            self.draw()

            if self.score > self.lowestHighScore:
                scoreString = 'Your score: ' + str(self.score) + '\n'
                if self.score > self.highestHighScore:
                    dialogText = scoreString + 'is a new high score, CONGRATULATIONS!'
                else:
                    dialogText = scoreString + 'gets you on the high scores list.'

                result = showCustomYesNoDialog(self.window, dialogText)
                if result:
                    self.goToScene(SCENE_HIGH_SCORES, self.score)

            self.newGameButton.enable()
            self.highScoresButton.enable()
            self.soundCheckBox.enable()
            self.quitButton.enable()

    def draw(self):
        self.window.fill(BLACK)
        self.oBaddieMgr.draw()
        self.oGoodieMgr.draw()
        self.oPowerUpMgr.draw()  # 추가
        self.oPlayer.draw()
        self.controlsBackground.draw()
        self.titleText.draw()
        self.scoreText.draw()
        self.highScoreText.draw()
        self.soundCheckBox.draw()
        self.quitButton.draw()
        self.highScoresButton.draw()
        self.newGameButton.draw()
        if self.playingState == STATE_GAME_OVER:
            self.gameOverImage.draw()

    def leave(self):
        pygame.mixer.music.stop()
    