##  Dodger main program
#
# Instantiates 3 scenes, creates and starts the scene manager
#
#  Original version by Al Sweigart from his book "Invent With Python"
#    (concept, graphics, and sounds used by permission from Al Sweigart)

# 1 - Import packages
import os
# The next line is here just in case you are running from the command line
os.chdir(os.path.dirname(os.path.abspath(__file__)))

import pygame
import pyghelpers
from SceneSplash import *
# from ScenePlay import * # ScenePlay는 직접 사용하지 않으므로 주석 처리 또는 삭제
from ScenePlayStage import ScenePlayStage # ScenePlayStage를 임포트
from SceneHighScores import *
from Constants import * # 추가 (WINDOW_WIDTH, WINDOW_HEIGHT 사용)

# 2 - Define constants
FRAMES_PER_SECOND = 40

# 3 - Initialize the world
pygame.init()
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

# 4 - Load assets: image(s), sounds,  etc.
# Make sure 'images/' and 'sounds/' directories exist and contain the required files.
# e.g., images/splashBackground.jpg, images/dodger.png, images/startNormal.png,
# images/quitNormal.png, images/gotoHighScoresNormal.png, images/player.png,
# images/baddie.png, images/goodie.png, sounds/background.mp3, sounds/gameOver.wav


# 5 - Initialize variables
# Instantiate all scenes and store them in a list
scenesList = [SceneSplash(window),
                    SceneHighScores(window),
                    ScenePlayStage(window)] # ScenePlayStage를 사용

# Create the scene manager, passing in the scenes list and the FPS
oSceneMgr = pyghelpers.SceneMgr(scenesList, FRAMES_PER_SECOND)

# Tell the Scene Manager to start running
oSceneMgr.run()
