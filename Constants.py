# Constants.py

# 게임 화면 크기
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600

# 게임 플레이 영역 크기 (UI가 상단에 있을 경우, 플레이어 움직임 제한 영역)
# Player.py에서 플레이어의 maxY 제한에 사용됩니다.
GAME_HEIGHT = 500
GAME_WIDTH = WINDOW_WIDTH # 게임 영역 너비는 창 너비와 동일

# 폰트 설정
FONT_NAME = 'malgungothic' # 시스템에 'malgungothic' 폰트가 있는지 확인

# 색상 정의 (RGB)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (150, 150, 150)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)


# --- 플레이어 관련 상수 ---
PLAYER_START_X = WINDOW_WIDTH // 2 # 플레이어 시작 X 위치 (화면 중앙)
PLAYER_START_Y = GAME_HEIGHT - 50 # 플레이어 시작 Y 위치 (게임 영역 하단에서 위로 50픽셀)
PLAYER_SPEED = 5 # (현재 마우스 제어이므로 직접 사용되지 않을 수 있음)


# --- 난이도 상수 (딕셔너리 키로 사용되므로 먼저 정의) ---
DIFFICULTY_EASY = 'easy'
DIFFICULTY_NORMAL = 'normal'
DIFFICULTY_HARD = 'hard'


# --- 게임 상태 상수 ---
STATE_WAITING = 'waiting'
STATE_PLAYING = 'playing'
STATE_PAUSED = 'paused'
STATE_GAME_OVER = 'gameOver' # 'game over' 대신 'gameOver'로 통일하여 사용


# --- 씬 키 상수 ---
SCENE_SPLASH = 'splash'
SCENE_PLAY_STAGE = 'playStage'
SCENE_PLAY_SURVIVAL = 'playSurvival'
SCENE_HIGH_SCORES = 'highScores'


# --- Baddies (적) 관련 상수 ---
BADDY_POINTS = 10 # Baddy와 충돌 시 잃는 점수
# BADDIE_STARTING_COUNT = 5 # (현재 BaddieMgr 로직에서는 사용되지 않음)

# Baddy 속도 기본값 (난이도 배율이 적용되기 전의 기준 속도)
BADDIE_MIN_SPEED_BASE = 2   # 적의 최소 초기 속도
BADDIE_MAX_SPEED_BASE = 5   # 적의 최대 초기 속도

# Baddy 속도 배율 (각 난이도별로 정의)
BADDY_SPEED_MULTIPLIER = {
    DIFFICULTY_EASY: 0.7,  # 쉬움: 기본 속도의 70%
    DIFFICULTY_NORMAL: 1.0, # 보통: 기본 속도의 100%
    DIFFICULTY_HARD: 1.3,  # 어려움: 기본 속도의 130%
}

# Baddy 생성 간격 (밀리초) - 값이 작을수록 자주 나타납니다.
BADDY_SPAWN_INTERVAL = {
    DIFFICULTY_EASY: 1000, # 1초마다
    DIFFICULTY_NORMAL: 700,  # 0.7초마다
    DIFFICULTY_HARD: 400,  # 0.4초마다
}


# --- Goodies (아이템) 관련 상수 ---
GOODIE_POINTS = 20 # Goodie를 얻었을 때 얻는 점수 (POINTS_FOR_GOODIE와 동일)

# Goodie 생성 간격 (밀리초) - 값이 작을수록 자주 나타납니다.
GOODIE_SPAWN_INTERVAL = {
    DIFFICULTY_EASY: 2000, # 2초마다
    DIFFICULTY_NORMAL: 1500, # 1.5초마다
    DIFFICULTY_HARD: 1000, # 1초마다
}


# --- 게임 모드별 상수 ---
GAME_DURATION_STAGE_MODE = 30000 # 스테이지 모드 게임 지속 시간 (30초)
SURVIVAL_TIME_LIMIT = 0 # 서바이벌 모드 시간 제한 (초, 0은 시간 제한 없음)

# 기존 Goodies 관련 상수 (프레임 단위) - 호환성을 위해 유지
GOODIE_SPAWN_INTERVAL_MAX = 100 # 프레임
GOODIE_SPAWN_INTERVAL_MIN = 50 # 프레임
GOODIE_INITIAL_RATE_LO = 50   # Goodie 생성 빈도 하한 (값이 작을수록 자주 나타남)
GOODIE_INITIAL_RATE_HI = 100  # Goodie 생성 빈도 상한 (값이 작을수록 자주 나타남)

# --- 기타 게임 관련 상수 ---
FRAMES_PER_SECOND = 60 # 초당 프레임 수


# --- 다이얼로그 관련 상수 ---
DIALOG_BOX_OFFSET = (WINDOW_WIDTH - 400) // 2 # 다이얼로그 박스의 X 오프셋 (너비 400 기준)
DIALOG_YES = 'Yes' # 'Yes' 버튼 응답 문자열
DIALOG_NO = 'No'   # 'No' 버튼 응답 문자열
DIALOG_ADD = 'Add' # 'Add' 버튼 응답 문자열 (하이 스코어 이름 입력 시)


# --- 최고 점수 시스템 관련 상수 ---
HIGH_SCORES_DATA = 'high_scores.json' # 최고 점수 데이터 파일 이름
HIGH_SCORES_TO_SAVE = 5 # 저장할 최고 점수 개수