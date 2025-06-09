#  Play scene - the main game play scene
# from pygame.locals import *

import pygame
import pygwidgets
import pyghelpers
import json
import os

from .objects import *
from src.Constants import *
from src.settings.SettingData import *

def showCustomYesNoDialog(theWindow, theText):
    oDialogBackground = pygwidgets.Image(theWindow, (40, 250),
                                            f'{RESOURCES_PATH}/images/dialog.png')
    oPromptDisplayText = pygwidgets.DisplayText(theWindow, (0, 290),
                                            theText, width=WINDOW_WIDTH,
                                            justified='center', fontSize=36)

    gth_PATH = f"{RESOURCES_PATH}/images/gotoHighScores"
    oYesButton = pygwidgets.CustomButton(theWindow, (320, 370),
                                            f'{gth_PATH}/gotoHighScoresNormal.png',
                                            over=f'{gth_PATH}/gotoHighScoresOver.png',
                                            down=f'{gth_PATH}/gotoHighScoresDown.png',
                                            disabled=f'{gth_PATH}/gotoHighScoresDisabled.png')

    nt_PATH = f"{RESOURCES_PATH}/images/noThanks"
    oNoButton = pygwidgets.CustomButton(theWindow, (62, 370),
                                            f'{nt_PATH}/noThanksNormal.png',
                                            over=f'{nt_PATH}/noThanksOver.png',
                                            down=f'{nt_PATH}/noThanksDown.png',
                                            disabled=f'{nt_PATH}/noThanksDisabled.png')

    choiceAsBoolean = pyghelpers.customYesNoDialog(theWindow,
                                            oDialogBackground, oPromptDisplayText,
                                            oYesButton, oNoButton)
    return choiceAsBoolean

BOTTOM_RECT = (0, GAME_HEIGHT + 1, WINDOW_WIDTH,
                                WINDOW_HEIGHT - GAME_HEIGHT)
STATE_WAITING = 'waiting'
STATE_PLAYING = 'playing'
STATE_GAME_OVER = 'game over'

class ScenePlay(pyghelpers.Scene):

    def __init__(self, window):
        self.window = window
        self.oSettingData = SettingData()
        
        # Initialize mixer first
        pygame.mixer.init()
        pygame.mixer.set_num_channels(8)  # Ensure enough channels for all sounds

        # UI Elements
        self.controlsBackground = pygwidgets.Image(self.window,
                                        (0, GAME_HEIGHT),
                                        f'{RESOURCES_PATH}/images/controlsBackground.jpg')

        qt_PATH = f"{RESOURCES_PATH}/images/quit"
        self.quitButton = pygwidgets.CustomButton(self.window,
                                        (30, GAME_HEIGHT + 90),
                                        up=f'{qt_PATH}/quitNormal.png',
                                        down=f'{qt_PATH}/quitDown.png',
                                        over=f'{qt_PATH}/quitOver.png',
                                        disabled=f'{qt_PATH}/quitDisabled.png')

        gth_PATH = f"{RESOURCES_PATH}/images/gotoHighScores"
        self.highScoresButton = pygwidgets.CustomButton(self.window,
                                        (190, GAME_HEIGHT + 90),
                                        up=f'{gth_PATH}/gotoHighScoresNormal.png',
                                        down=f'{gth_PATH}/gotoHighScoresDown.png',
                                        over=f'{gth_PATH}/gotoHighScoresOver.png',
                                        disabled=f'{gth_PATH}/gotoHighScoresDisabled.png')

        stn_PATH = f"{RESOURCES_PATH}/images/startNew"
        self.newGameButton = pygwidgets.CustomButton(self.window,
                                        (450, GAME_HEIGHT + 90),
                                        up=f'{stn_PATH}/startNewNormal.png',
                                        down=f'{stn_PATH}/startNewDown.png',
                                        over=f'{stn_PATH}/startNewOver.png',
                                        disabled=f'{stn_PATH}/startNewDisabled.png',
                                        enterToActivate=True)

        self.settingButton = pygwidgets.CustomButton(self.window,
                                        (430, GAME_HEIGHT + 17),
                                        up=f'{RESOURCES_PATH}/images/setting.png')

        self.gameOverImage = pygwidgets.Image(self.window, (140, 180),
                                        f'{RESOURCES_PATH}/images/gameOver.png')

        self.titleText = pygwidgets.DisplayText(self.window,
                                        (70, GAME_HEIGHT + 17),
                                        'Score:                                 High Score:',
                                        fontSize=24, textColor=WHITE)

        self.scoreText = pygwidgets.DisplayText(self.window,
                                        (80, GAME_HEIGHT + 47), '0',
                                        fontSize=36, textColor=WHITE,
                                        justified='right')

        self.highScoreText = pygwidgets.DisplayText(self.window,
                                        (270, GAME_HEIGHT + 47), '',
                                        fontSize=36, textColor=WHITE,
                                        justified='right')
        
        # Load sounds
        try:
            # Sound Resources PATH
            snd_PATH = f"{RESOURCES_PATH}/sounds"
            
            # Background music
            pygame.mixer.music.load(f'{snd_PATH}/background.mid')
            
            # Sound effects
            self.dingSound = pygame.mixer.Sound(f'{snd_PATH}/ding.wav')
            self.gameOverSound = pygame.mixer.Sound(f'{snd_PATH}/gameover.wav')
            
        except Exception as e:
            print(f"Error loading sounds: {e}")
            self.dingSound = None
            self.gameOverSound = None
        
        # Instantiate objects
        self.oPlayer = Player(self.window)
        self.oBaddieMgr = BaddieMgr(self.window)
        self.oGoodieMgr = GoodieMgr(self.window)

        self.highestHighScore = 0
        self.lowestHighScore = 0
        self.score = 0
        self.playingState = STATE_WAITING

    def getSceneKey(self):
        return SCENE_PLAY

    def updateSoundVolumes(self):
        try:
            settings = self.oSettingData.getSetting()
            
            # Convert to float for pygame (0.0-1.0)
            bg_volume = settings['sound']['background']['volume'] / 100.0
            # 이펙트 사운드 볼륨을 1.5배 증가
            effects_volume = (settings['sound']['effects']['volume'] / 100.0) * 1.5
            bg_playing = settings['sound']['background']['playing']
            
            # Set background music volume
            pygame.mixer.music.set_volume(bg_volume)
            
            # Set sound effects volumes
            self.dingSound.set_volume(effects_volume)
            self.gameOverSound.set_volume(effects_volume)
                
            # Update music playback based on playing status
            if not bg_playing:
                pygame.mixer.music.pause()
            else:
                pygame.mixer.music.unpause()
                
        except Exception as e:
            print(f"Error updating volumes: {e}")

    def enter(self, data):
        self.getHiAndLowScores()
        
        # 먼저 현재 재생 중인 음악을 정지
        pygame.mixer.music.stop()
        
        # 새로운 설정으로 소리 업데이트
        self.updateSoundVolumes()
        
        # 배경음악 재생 상태에 따라 재생
        if self.oSettingData.getSetting()['sound']['background']['playing']:
            try:
                pygame.mixer.music.play(-1, 0.0)
            except Exception as e:
                print(f"Error playing background music: {e}")

    def getHiAndLowScores(self):
        infoDict = self.request(SCENE_HIGH_SCORES, HIGH_SCORES_DATA)
        self.highestHighScore = infoDict['highest']
        self.highScoreText.setValue(self.highestHighScore)
        self.lowestHighScore = infoDict['lowest']

    def reset(self):   # start a new game
        self.score = 0
        self.scoreText.setValue(self.score)
        self.getHiAndLowScores()

        # Tell the managers to reset themselves
        self.oBaddieMgr.reset()
        self.oGoodieMgr.reset()

        self.updateSoundVolumes()
        if self.oSettingData.getSetting()['sound']['background']['playing']:
            try:
                pygame.mixer.music.play(-1, 0.0)
            except Exception as e:
                print(f"Error playing background music: {e}")
        else:
            pygame.mixer.music.stop()

        self.newGameButton.disable()
        self.highScoresButton.disable()
        self.quitButton.disable()
        pygame.mouse.set_visible(False)

    def handleInputs(self, eventsList, keyPressedList):
        if self.playingState == STATE_PLAYING:
            return  # ignore button events while playing

        for event in eventsList:
            if self.newGameButton.handleEvent(event):
                self.reset()
                self.playingState = STATE_PLAYING

            if self.highScoresButton.handleEvent(event):
                self.goToScene(SCENE_HIGH_SCORES)

            if self.settingButton.handleEvent(event):
                self.goToScene(SCENE_SETTING)
            
            if self.quitButton.handleEvent(event):
                self.quit()

    def update(self):
        self.updateSoundVolumes()

        if self.playingState != STATE_PLAYING:
            return  # only update game logic when playing

        # Move the Player to the mouse position, get back its rect
        mouseX, mouseY = pygame.mouse.get_pos()
        playerRect = self.oPlayer.update(mouseX, mouseY)

        # Tell the GoodieMgr to move all Goodies
        # Returns the number of Goodies that the Player contacted
        nGoodiesHit = self.oGoodieMgr.update(playerRect)
        if nGoodiesHit > 0 and self.dingSound:
            try:
                self.dingSound.play()
            except Exception as e:
                print(f"Error playing ding sound: {e}")
            self.score = self.score + (nGoodiesHit * POINTS_FOR_GOODIE)

        # Tell the BaddieMgr to move all the Baddies
        # Returns the number of Baddies that fell off the bottom
        nBaddiesEvaded = self.oBaddieMgr.update()
        self.score = self.score + (nBaddiesEvaded * POINTS_FOR_BADDIE_EVADED)
        
        self.scoreText.setValue(self.score)

        # Check if the Player has hit any Baddie
        if self.oBaddieMgr.hasPlayerHitBaddie(playerRect):
            pygame.mouse.set_visible(True)
            pygame.mixer.music.stop()

            if self.gameOverSound:
                try:
                    self.gameOverSound.play()
                except Exception as e:
                    print(f"Error playing game over sound: {e}")
            self.playingState = STATE_GAME_OVER
            self.draw()  # force drawing of game over message

            if self.score > self.lowestHighScore:
                scoreString = 'Your score: ' + str(self.score) + '\n'
                if self.score > self.highestHighScore:
                    dialogText = (scoreString +
                                       'is a new high score, CONGRATULATIONS!')
                else:
                    dialogText = (scoreString +
                                      'gets you on the high scores list.')

                result = showCustomYesNoDialog(self.window, dialogText)
                if result: # navigate
                    self.goToScene(SCENE_HIGH_SCORES, self.score)

            self.newGameButton.enable()
            self.highScoresButton.enable()
            self.quitButton.enable()
    
    def draw(self):
        self.window.fill(BLACK)
    
        # Tell the managers to draw all the Baddies and Goodies
        self.oBaddieMgr.draw()
        self.oGoodieMgr.draw()
    
        # Tell the Player to draw itself
        self.oPlayer.draw()
    
        # Draw all the info at the bottom of the window
        self.controlsBackground.draw()
        self.titleText.draw()
        self.scoreText.draw()
        self.highScoreText.draw()
        self.settingButton.draw()
        self.quitButton.draw()
        self.highScoresButton.draw()
        self.newGameButton.draw()

        if self.playingState == STATE_GAME_OVER:
            self.gameOverImage.draw()

    def leave(self):
        pygame.mixer.music.stop()
