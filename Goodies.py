# Goodie and GoddieMgr classes
import pygame
import pygwidgets
import random
from Constants import * # 추가

# Goodie and GoddieMgr classes
import pygame
import pygwidgets
import random
from Constants import *

class Goodie():
    MIN_SIZE = 10
    MAX_SIZE = 40
    MIN_SPEED = 1
    MAX_SPEED = 8
    # Load the image once
    GOODIE_IMAGE = pygame.image.load('images/goodie.png')
    RIGHT = 'right'
    LEFT = 'left'

    def __init__(self, window):
        self.window = window
        size = random.randrange(Goodie.MIN_SIZE, Goodie.MAX_SIZE + 1)
        self.y = random.randrange(0, GAME_HEIGHT - size)

        self.direction = random.choice([Goodie.LEFT, Goodie.RIGHT])
        if self.direction == Goodie.LEFT:  # start on right side of the window
            self.x = WINDOW_WIDTH
            self.speed = - random.randrange(Goodie.MIN_SPEED,
                                                            Goodie.MAX_SPEED + 1)
            self.minLeft = - size
        else:  # start on left side of the window
            self.x = 0 - size
            self.speed = random.randrange(Goodie.MIN_SPEED,
                                                          Goodie.MAX_SPEED + 1)

        self.image = pygwidgets.Image(self.window,
                                                     (self.x, self.y), Goodie.GOODIE_IMAGE)
        percent = int((size * 100) / Goodie.MAX_SIZE)
        self.image.scale(percent, False)

    def update(self):
        self.x = self.x + self.speed
        self.image.setLoc((self.x, self.y))
        if self.direction == Goodie.LEFT:
            if self.x < self.minLeft:
                return True  # needs to be deleted
            else:
                return False  # stays in window
        else:
            if self.x > WINDOW_WIDTH:
                return True  # needs to be deleted
            else:
                return False  # stays in window

    def draw(self):
        self.image.draw()

    def collide(self, playerRect):
        collidedWithPlayer = self.image.overlaps(playerRect)
        return collidedWithPlayer


class GoodieMgr():
    INITIAL_GOODIE_RATE_LO = 90 # 초기 최소 생성 간격
    INITIAL_GOODIE_RATE_HI = 111 # 초기 최대 생성 간격
    RATE_DECREMENT_PER_STAGE = 5 # 스테이지당 생성 간격 감소량

    def __init__(self, window):
        self.window = window
        self.reset()

    def reset(self):  # Called when starting a new game
        self.goodiesList = []
        self.current_goodie_rate_lo = GoodieMgr.INITIAL_GOODIE_RATE_LO
        self.current_goodie_rate_hi = GoodieMgr.INITIAL_GOODIE_RATE_HI
        self.nFramesTilNextGoodie = random.randrange(self.current_goodie_rate_lo,
                                                     self.current_goodie_rate_hi)

    def update(self, thePlayerRect):
        # Tell each Goodie to update itself.
        # If a Goodie goes off an edge, remove it
        # Count up all Goodies that contact the player and remove them.
        nGoodiesHit = 0
        goodiesListCopy = self.goodiesList.copy()
        for oGoodie in goodiesListCopy:
            deleteMe = oGoodie.update()
            if deleteMe:
                self.goodiesList.remove(oGoodie)  # remove this Goodie

            elif oGoodie.collide(thePlayerRect):
                self.goodiesList.remove(oGoodie)  # remove this Goodie
                nGoodiesHit = nGoodiesHit + 1
        
        # If the correct amount of frames have passed,
        # add a new Goodie (and reset the counter)
        self.nFramesTilNextGoodie = self.nFramesTilNextGoodie - 1
        if self.nFramesTilNextGoodie == 0:
            oGoodie = Goodie(self.window)
            self.goodiesList.append(oGoodie)
            self.nFramesTilNextGoodie = random.randrange(
                                                            self.current_goodie_rate_lo,
                                                            self.current_goodie_rate_hi)

        return nGoodiesHit  # return number of Goodies that contacted player

    def draw(self):
        for oGoodie in self.goodiesList:
            oGoodie.draw()

    def increaseFrequency(self, stage):
        # 스테이지가 올라갈수록 굿디 생성 빈도 증가 (RATE_LO, RATE_HI 감소)
        # 최소값을 설정하여 너무 빨라지지 않도록 합니다.
        self.current_goodie_rate_lo = max(10, GoodieMgr.INITIAL_GOODIE_RATE_LO - (stage - 1) * GoodieMgr.RATE_DECREMENT_PER_STAGE)
        self.current_goodie_rate_hi = max(15, GoodieMgr.INITIAL_GOODIE_RATE_HI - (stage - 1) * GoodieMgr.RATE_DECREMENT_PER_STAGE)
        
        # 최소값이 최대값보다 커지지 않도록 보정
        if self.current_goodie_rate_lo > self.current_goodie_rate_hi:
            self.current_goodie_rate_lo = self.current_goodie_rate_hi - 5 # 최소 5프레임 차이 유지 (조정 가능)
            if self.current_goodie_rate_lo < 1: # 최소값이 1 미만이 되지 않도록
                self.current_goodie_rate_lo = 1