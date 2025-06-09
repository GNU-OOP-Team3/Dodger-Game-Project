# Constants - used by multiple Python files
import os
import pygame

# PATH
# ROOT Directory
ROOT_PATH = os.path.dirname(os.path.dirname(__file__))
RESOURCES_PATH = os.path.join(ROOT_PATH, 'resources')

WINDOW_WIDTH = 600
WINDOW_HEIGHT = 700
GAME_HEIGHT = 560
DIALOG_BOX_OFFSET = 35
DIALOG_BOX_WIDTH = WINDOW_WIDTH - (2 * DIALOG_BOX_OFFSET)

# Scene keys
SCENE_SPLASH = 'scene splash'
SCENE_PLAY = 'scene play'
SCENE_HIGH_SCORES = 'scene high scores'
SCENE_SETTING = 'scene setting'

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

POINTS_FOR_GOODIE = 25
POINTS_FOR_BADDIE_EVADED = 1
HIGH_SCORES_DATA = 'high scores data'

N_HIGH_SCORES = 10

SETTING_DATA = 'setting data'

# Tuple of legal editing keys
LEGAL_KEYS_TUPLE = (pygame.K_RIGHT, pygame.K_LEFT, pygame.K_HOME,
                    pygame.K_END, pygame.K_DELETE, pygame.K_BACKSPACE, 
                    pygame.K_RETURN, pygame.K_KP_ENTER)
# Legal keys to be typed
LEGAL_UNICODE_CHARS = ('0123456789.-')
