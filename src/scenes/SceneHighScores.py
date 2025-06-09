# High Scores scene
import pygwidgets
import pyghelpers
from src.scores.HighScoresData import *

def showCustomAnswerDialog(theWindow, theText):
    oDialogBackground = pygwidgets.Image(theWindow, (35, 450),
                                                f'{RESOURCES_PATH}/images/dialog.png')
    
    oPromptDisplayText = pygwidgets.DisplayText(theWindow, (0, 480),
                                                theText, width=WINDOW_WIDTH,
                                                justified='center', fontSize=36)
    
    oUserInputText = pygwidgets.InputText(theWindow, (200, 550), '',
                                                fontSize=36, initialFocus=True)
    
    nt_PATH = f"{RESOURCES_PATH}/images/noThanks"
    oNoButton = pygwidgets.CustomButton(theWindow, (65, 595),
                                                f'{nt_PATH}/noThanksNormal.png',
                                                over=f'{nt_PATH}/noThanksOver.png',
                                                down=f'{nt_PATH}/noThanksDown.png',
                                                disabled=f'{nt_PATH}/noThanksDisabled.png')
    
    ad_PATH = f"{RESOURCES_PATH}/images/add"
    oYesButton = pygwidgets.CustomButton(theWindow, (330, 595),
                                                f'{ad_PATH}/addNormal.png',
                                                over=f'{ad_PATH}/addOver.png',
                                                down=f'{ad_PATH}/addDown.png',
                                                disabled=f'{ad_PATH}/addDisabled.png')
    
    userAnswer = pyghelpers.customAnswerDialog(theWindow,
                                                oDialogBackground,
                                                oPromptDisplayText, oUserInputText,
                                                oYesButton, oNoButton)
    return userAnswer

def showCustomResetDialog(theWindow, theText):
    oDialogBackground = pygwidgets.Image(theWindow,
                                               (35, 450), f'{RESOURCES_PATH}/images/dialog.png')
    
    oPromptDisplayText = pygwidgets.DisplayText(theWindow, (0, 480),
                                                theText, width=WINDOW_WIDTH,
                                                justified='center', fontSize=36)
    
    cn_PATH = f"{RESOURCES_PATH}/images/cancel"
    oNoButton = pygwidgets.CustomButton(theWindow, (65, 595),
                                                f'{cn_PATH}/cancelNormal.png',
                                                over=f'{cn_PATH}/cancelOver.png',
                                                down=f'{cn_PATH}/cancelDown.png',
                                                disabled=f'{cn_PATH}/cancelDisabled.png')
    
    ok_PATH = f"{RESOURCES_PATH}/images/ok"
    oYesButton = pygwidgets.CustomButton(theWindow, (330, 595),
                                                f'{ok_PATH}/okNormal.png',
                                                over=f'{ok_PATH}/okOver.png',
                                                down=f'{ok_PATH}/okDown.png',
                                                disabled=f'{ok_PATH}/okDisabled.png')
    
    choiceAsBoolean = pyghelpers.customYesNoDialog(theWindow,
                                                oDialogBackground, oPromptDisplayText,
                                                oYesButton, oNoButton)
    return choiceAsBoolean


class SceneHighScores(pyghelpers.Scene):
    def __init__(self, window):
        self.window = window
        self.oHighScoresData = HighScoresData()
        
        self.backgroundImage = pygwidgets.Image(self.window,
                                                (0, 0),
                                                f'{RESOURCES_PATH}/images/highScoresBackground.jpg')

        self.namesField = pygwidgets.DisplayText(self.window, (260, 84), '',
                                                   fontSize=48, textColor=BLACK,
                                                   width=300, justified='left')
        self.scoresField = pygwidgets.DisplayText(self.window,
                                                  (25, 84), '', fontSize=48,
                                                  textColor=BLACK,
                                                  width=175, justified='right')

        qt_PATH = f"{RESOURCES_PATH}/images/quit"
        self.quitButton = pygwidgets.CustomButton(self.window,
                                                  (30, 650),
                                                  up=f'{qt_PATH}/quitNormal.png',
                                                  down=f'{qt_PATH}/quitDown.png',
                                                  over=f'{qt_PATH}/quitOver.png',
                                                  disabled=f'{qt_PATH}/quitDisabled.png')

        bk_PATH = f"{RESOURCES_PATH}/images/back"
        self.backButton = pygwidgets.CustomButton(self.window,
                                                 (240, 650),
                                                 up=f'{bk_PATH}/backNormal.png',
                                                 down=f'{bk_PATH}/backDown.png',
                                                 over=f'{bk_PATH}/backOver.png',
                                                 disabled=f'{bk_PATH}/backDisabled.png')

        rs_PATH = f"{RESOURCES_PATH}/images/reset"
        self.resetScoresButton = pygwidgets.CustomButton(self.window,
                                                 (450, 650),
                                                 up=f'{rs_PATH}/resetNormal.png',
                                                 down=f'{rs_PATH}/resetDown.png',
                                                 over=f'{rs_PATH}/resetOver.png',
                                                 disabled=f'{rs_PATH}/resetDisabled.png')

        self.showHighScores()

    def getSceneKey(self):
        return SCENE_HIGH_SCORES

    def enter(self, newHighScoreValue=None):
        # This can be called two different ways:
        # 1. If no new high score, newHighScoreValue will be None
        # 2. newHighScoreValue is score of the current game - in top 10
        if newHighScoreValue is None:
            return  # nothing to do

        self.draw() # draw before showing dialog
        # We have a new high score sent in from the Play scene
        dialogQuestion = ('To record your score of ' +
                                 str(newHighScoreValue) + ',\n' +
                                 'please enter your name:')
        playerName = showCustomAnswerDialog(self.window,
                                                                    dialogQuestion)
        if playerName is None:
            return  # user pressed Cancel

        # Add user and score to high scores
        if playerName == '':
            playerName = 'Anonymous'
        self.oHighScoresData.addHighScore(playerName,
                                                            newHighScoreValue)

        # Show the updated high scores table
        self.showHighScores()

    def showHighScores(self):
        # Get the scores and names, show them in two fields
        scoresList, namesList = self.oHighScoresData.getScoresAndNames()
        self.namesField.setValue(namesList)
        self.scoresField.setValue(scoresList)        

    def handleInputs(self, eventsList, keyPressedList):
        for event in eventsList:
            if self.quitButton.handleEvent(event):
                self.quit()

            elif self.backButton.handleEvent(event):
                self.goToScene(SCENE_PLAY)

            elif self.resetScoresButton.handleEvent(event):
                confirmed = showCustomResetDialog(self.window,
                                        'Are you sure you want to \nRESET the high scores?')
                if confirmed:
                    self.oHighScoresData.resetScores()
                    self.showHighScores()

    def draw(self):
        self.backgroundImage.draw()
        self.scoresField.draw()
        self.namesField.draw()
        self.quitButton.draw()
        self.resetScoresButton.draw()
        self.backButton.draw()

    def respond(self, requestID):
        if requestID == HIGH_SCORES_DATA:
            # Request from Play scene for the highest and lowest scores
            # Build a dictionary and return it to the Play scene
            highestScore, lowestScore = self.oHighScoresData.getHighestAndLowest()
            return {'highest':highestScore, 'lowest':lowestScore}
