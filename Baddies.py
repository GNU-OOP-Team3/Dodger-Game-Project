# Baddie and BaddieMgr classes

import pygame
import pygwidgets
import random
from Constants import *

# Baddie class
class Baddie():
    MIN_SIZE = 10
    MAX_SIZE = 40
    MIN_SPEED = 1
    MAX_SPEED = 8
    # Load the image only once
    BADDIE_IMAGE = pygame.image.load('images/baddie.png')

    def __init__(self, window, speed_min=None, speed_max=None): # speed_min, speed_max 추가
        self.window = window
        # Create the image object
        size = random.randrange(Baddie.MIN_SIZE, Baddie.MAX_SIZE + 1)
        self.x = random.randrange(0, WINDOW_WIDTH - size)
        self.y = 0 - size # start above the window
        self.image = pygwidgets.Image(self.window, (self.x, self.y),
                                      Baddie.BADDIE_IMAGE)

        # Scale it
        percent = (size * 100) / Baddie.MAX_SIZE
        self.image.scale(percent, False)
        
        # 난이도에 따라 속도 조절
        if speed_min is not None and speed_max is not None:
            self.speed = random.randrange(speed_min, speed_max + 1)
        else:
            self.speed = random.randrange(Baddie.MIN_SPEED,
                                                          Baddie.MAX_SPEED + 1)

    def update(self):  # move the Baddie down
        self.y = self.y + self.speed
        self.image.setLoc((self.x, self.y))
        if self.y > GAME_HEIGHT:
            return True  # needs to be deleted
        else:
            return False  # stays in the window

    def draw(self):
        self.image.draw()

    def collide(self, playerRect):
        collidedWithPlayer = self.image.overlaps(playerRect)
        return collidedWithPlayer

# BaddieMgr class
class BaddieMgr():
    INITIAL_ADD_NEW_BADDIE_RATE = 8  # 초기 배디 생성 빈도
    INITIAL_MIN_SPEED = 1
    INITIAL_MAX_SPEED = 8
    SPEED_INCREMENT_PER_STAGE = 0.5 # 스테이지당 속도 증가량

    def __init__(self, window):
        self.window = window
        self.reset()

    def reset(self):  # called when starting a new game
        self.baddiesList = []
        self.nFramesTilNextBaddie = BaddieMgr.INITIAL_ADD_NEW_BADDIE_RATE
        self.current_add_rate = BaddieMgr.INITIAL_ADD_NEW_BADDIE_RATE
        self.current_min_speed = BaddieMgr.INITIAL_MIN_SPEED
        self.current_max_speed = BaddieMgr.INITIAL_MAX_SPEED

    def update(self):
        # Tell each Baddie to update itself
        # Count how many Baddies have fallen off the bottom.
        nBaddiesRemoved = 0
        baddiesListCopy = self.baddiesList.copy()
        for oBaddie in baddiesListCopy:
            deleteMe = oBaddie.update()
            if deleteMe:
                self.baddiesList.remove(oBaddie)
                nBaddiesRemoved = nBaddiesRemoved + 1

        # Check if it's time to add a new Baddie
        self.nFramesTilNextBaddie = self.nFramesTilNextBaddie - 1
        if self.nFramesTilNextBaddie == 0:
            # 현재 난이도 설정에 따라 배디 생성
            oBaddie = Baddie(self.window, self.current_min_speed, self.current_max_speed)
            self.baddiesList.append(oBaddie)
            self.nFramesTilNextBaddie = int(self.current_add_rate) # 정수로 변환

        # Return that count of Baddies that were removed
        return nBaddiesRemoved

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
        self.current_min_speed = int(self.current_min_speed)
        self.current_max_speed = int(self.current_max_speed)
        
        # 최소 속도가 최대 속도를 넘지 않도록 보정
        if self.current_min_speed > self.current_max_speed:
            self.current_min_speed = self.current_max_speed - 1
            if self.current_min_speed < 1: # 최소 속도가 1 미만이 되지 않도록
                self.current_min_speed = 1

