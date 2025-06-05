# Constants - used by multiple Python files

WINDOW_WIDTH = 600
WINDOW_HEIGHT = 700
GAME_HEIGHT = 560
DIALOG_BOX_OFFSET = 35
DIALOG_BOX_WIDTH = WINDOW_WIDTH - (2 * DIALOG_BOX_OFFSET)

# Scene keys
SCENE_SPLASH = 'scene splash'
SCENE_PLAY = 'scene play'
SCENE_PLAY_STAGE = 'scene play stage' # 기존 SCENE_PLAY를 더 명확하게 변경
SCENE_PLAY_SURVIVAL = 'scene play survival' # 서바이벌 모드 씬 키 추가
SCENE_HIGH_SCORES = 'scene high scores'

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

POINTS_FOR_GOODIE = 25
POINTS_FOR_BADDIE_EVADED = 1
HIGH_SCORES_DATA = 'high scores data'
N_HIGH_SCORES = 10

# Game states
STATE_WAITING = 'waiting'
STATE_PLAYING = 'playing'
STATE_GAME_OVER = 'game over'