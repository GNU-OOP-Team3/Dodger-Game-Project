# Main_Dodger.py
import pygame
import pyghelpers
from Constants import (WINDOW_WIDTH, WINDOW_HEIGHT, FRAMES_PER_SECOND,
                        SCENE_SPLASH, SCENE_PLAY_STAGE, SCENE_PLAY_SURVIVAL, SCENE_HIGH_SCORES)

from SceneSplash import SceneSplash
from ScenePlayStage import ScenePlayStage
from ScenePlaySurvival import ScenePlaySurvival
from SceneHighScores import SceneHighScores

pygame.init()
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Dodger Game')

# --- 이 부분이 중요합니다! 각 씬 클래스를 인스턴스화(객체 생성) 해야 합니다. ---
oSplashScene = SceneSplash(window)
oPlayStageScene = ScenePlayStage(window)
oPlaySurvivalScene = ScenePlaySurvival(window)
oHighScoresScene = SceneHighScores(window)

# 씬 매니저에 씬 객체 리스트를 추가합니다.
oSceneMgr = pyghelpers.SceneMgr(SCENE_SPLASH, [oSplashScene,
                                                oPlayStageScene,
                                                oPlaySurvivalScene,
                                                oHighScoresScene])

# 게임 루프 실행
oSceneMgr.run()