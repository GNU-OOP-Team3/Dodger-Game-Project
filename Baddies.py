# Baddie and BaddieMgr classes

import pygame
import pygwidgets
import random
from Constants import * # Constants.py에서 상수들을 임포트

# Baddie class
class Baddie():
    MIN_SIZE = 10
    MAX_SIZE = 40
    MIN_SPEED=1
    MAX_SPEED=8
    # BADDIE_IMAGE는 모든 Baddie 인스턴스에서 공유되도록 클래스 변수로 로드
    BADDIE_IMAGE = pygame.image.load('images/baddie.png')

    def __init__(self, window, speed_min=None, speed_max=None):
        self.window = window
        # 이미지 크기를 랜덤으로 설정
        size = random.randrange(Baddie.MIN_SIZE, Baddie.MAX_SIZE + 1)
        self.x = random.randrange(0, WINDOW_WIDTH - size) # 화면 상단에 랜덤 X 위치
        self.y = 0 - size # 화면 위에서 시작

        # pygwidgets.Image로 Baddie 이미지 생성
        self.image = pygwidgets.Image(self.window, (self.x, self.y), Baddie.BADDIE_IMAGE)
        # 이미지 크기 조절
        percent = (size * 100) / Baddie.MAX_SIZE
        self.image.scale(percent, False) # 가로세로 비율 유지

        # 난이도에 따라 속도 조절. BaddieMgr에서 전달받은 값이 없으면 기본값 사용.
        if speed_min is not None and speed_max is not None:
            self.speed = random.randrange(speed_min, speed_max + 1)
        else:
            # 기본 속도 (BaddieMgr에서 초기화 시 사용될 수 있음)
            self.speed = random.randrange(BaddieMgr.INITIAL_MIN_SPEED, BaddieMgr.INITIAL_MAX_SPEED + 1)


    def update(self):  # 배디를 아래로 이동
        self.y = self.y + self.speed
        self.image.setLoc((self.x, self.y))

    def draw(self):
        self.image.draw()

    def collide(self, playerRect): # 플레이어와 충돌했는지 확인
        return self.image.getRect().colliderect(playerRect)

# BaddieMgr class - Baddie 객체들을 관리
class BaddieMgr():
    INITIAL_ADD_NEW_BADDIE_RATE = 20 # 초기 배디 생성 주기 (프레임 단위)
    SPEED_INCREMENT_PER_STAGE = 1 # 스테이지마다 속도 증가량

    # Baddie의 초기 최소/최대 속도 (난이도 조절의 기준점)
    # Constants.py에 정의된 상수를 Baddie 클래스에서 직접 참조하도록 변경 가능
    INITIAL_MIN_SPEED = Baddie.MIN_SPEED # Baddie 클래스의 MIN_SPEED 사용
    INITIAL_MAX_SPEED = Baddie.MAX_SPEED # Baddie 클래스의 MAX_SPEED 사용

    def __init__(self, window):
        self.window = window
        self.baddiesList = []
        self.nFramesTilNextBaddie = 0

        # 초기 난이도 설정을 위한 변수들 (resetDifficultySettings에서 활용)
        self.initial_add_rate = BaddieMgr.INITIAL_ADD_NEW_BADDIE_RATE
        self.initial_min_speed = BaddieMgr.INITIAL_MIN_SPEED
        self.initial_max_speed = BaddieMgr.INITIAL_MAX_SPEED
        
        self.resetDifficultySettings() # 초기 설정 적용

    def reset(self): # 게임 리셋 시 호출. Baddie 리스트 초기화.
        self.baddiesList = []
        self.nFramesTilNextBaddie = 0
        self.resetDifficultySettings() # 난이도 설정을 초기 상태로 되돌림

    def resetDifficultySettings(self): # 현재 난이도 설정을 초기화 (새로운 난이도 적용 시 호출)
        self.current_add_rate = self.initial_add_rate
        self.current_min_speed = self.initial_min_speed
        self.current_max_speed = self.initial_max_speed

    def setDifficultySpeeds(self, min_speed, max_speed): # 난이도에 따라 속도 설정
        self.initial_min_speed = min_speed
        self.initial_max_speed = max_speed
        self.resetDifficultySettings() # 새 속도로 재설정

    def update(self):
        nBaddiesRemoved = 0
        baddiesToKeep = [] # 화면에 남길 배디들을 저장할 리스트

        for oBaddie in self.baddiesList:
            oBaddie.update()
            # 배디가 화면 아래로 벗어나면 제거
            if oBaddie.y < WINDOW_HEIGHT:
                baddiesToKeep.append(oBaddie)
            else:
                nBaddiesRemoved = nBaddiesRemoved + 1
        
        self.baddiesList = baddiesToKeep # 화면에 남은 배디들만 다시 리스트에 할당

        # 배디 생성 주기 관리
        self.nFramesTilNextBaddie = self.nFramesTilNextBaddie - 1
        if self.nFramesTilNextBaddie == 0:
            # 현재 난이도 설정에 따른 속도로 새로운 배디 생성
            oBaddie = Baddie(self.window, self.current_min_speed, self.current_max_speed)
            self.baddiesList.append(oBaddie)
            # 다음 배디 생성까지의 프레임 수 재설정 (현재 생성 주기에 따름)
            self.nFramesTilNextBaddie = int(self.current_add_rate)

        return nBaddiesRemoved  # 플레이어가 피한 배디 수 반환

    def draw(self):
        for oBaddie in self.baddiesList:
            oBaddie.draw()

    def hasPlayerHitBaddie(self, playerRect):
        for oBaddie in self.baddiesList:
            if oBaddie.collide(playerRect):
                return True
        return False

    def increaseDifficulty(self, stage):
        # 스테이지가 올라갈수록 배디 생성 빈도 증가 (ADD_NEW_BADDIE_RATE 감소)
        # 최소값을 설정하여 너무 빨라지지 않도록 합니다.
        self.current_add_rate = max(1, BaddieMgr.INITIAL_ADD_NEW_BADDIE_RATE - (stage - 1))

        # 스테이지가 올라갈수록 배디 속도 증가
        self.current_min_speed = BaddieMgr.INITIAL_MIN_SPEED + (stage - 1) * BaddieMgr.SPEED_INCREMENT_PER_STAGE
        self.current_max_speed = BaddieMgr.INITIAL_MAX_SPEED + (stage - 1) * BaddieMgr.SPEED_INCREMENT_PER_STAGE

        # 속도 최소값과 최대값 설정 (선택 사항)
        # 속도가 너무 커지지 않도록 최대 속도 제한을 고려할 수 있습니다.
        self.current_min_speed = int(self.current_min_speed)
        self.current_max_speed = int(self.current_max_speed)