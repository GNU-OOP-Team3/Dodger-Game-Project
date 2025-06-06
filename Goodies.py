# Goodie and GoodieMgr classes

import pygame
import pygwidgets
import random
from Constants import * # Constants.py에서 상수들을 임포트

# Goodie class
class Goodie():
    MIN_SIZE = 10
    MAX_SIZE = 40
    MIN_SPEED = 1
    MAX_SPEED = 8
    # GOODIE_IMAGE는 모든 Goodie 인스턴스에서 공유되도록 클래스 변수로 로드
    GOODIE_IMAGE = pygame.image.load('images/goodie.png')
    RIGHT = 'right'
    LEFT = 'left'

    def __init__(self, window):
        self.window = window
        # 이미지 크기 랜덤 설정
        size = random.randrange(Goodie.MIN_SIZE, Goodie.MAX_SIZE + 1)
        self.y = random.randrange(0, GAME_HEIGHT - size) # 게임 영역 내 랜덤 Y 위치

        # 랜덤 방향 (왼쪽에서 오거나 오른쪽에서 오거나)
        self.direction = random.choice([Goodie.LEFT, Goodie.RIGHT])
        if self.direction == Goodie.LEFT:  # 오른쪽에서 시작 (왼쪽으로 이동)
            self.x = WINDOW_WIDTH
            self.speed = - random.randrange(Goodie.MIN_SPEED, Goodie.MAX_SPEED + 1)
            self.minLeft = - size # 화면 밖으로 완전히 나가는 최소 X 값
        else:  # 왼쪽에서 시작 (오른쪽으로 이동)
            self.x = 0 - size
            self.speed = random.randrange(Goodie.MIN_SPEED, Goodie.MAX_SPEED + 1)

        # pygwidgets.Image로 Goodie 이미지 생성
        self.image = pygwidgets.Image(self.window, (self.x, self.y), Goodie.GOODIE_IMAGE)
        # 이미지 크기 조절
        percent = int((size * 100) / Goodie.MAX_SIZE)
        self.image.scale(percent, False) # 가로세로 비율 유지

    def update(self):  # 굿디 이동
        self.x = self.x + self.speed
        self.image.setLoc((self.x, self.y))

    def draw(self):
        self.image.draw()

    def collide(self, playerRect): # 플레이어와 충돌했는지 확인
        return self.image.getRect().colliderect(playerRect)

# GoodieMgr class - Goodie 객체들을 관리
class GoodieMgr():
    INITIAL_GOODIE_RATE_LO = 30 # 굿디 생성 주기 하한 (프레임 단위)
    INITIAL_GOODIE_RATE_HI = 60 # 굿디 생성 주기 상한 (프레임 단위)
    RATE_DECREMENT_PER_STAGE = 5 # 스테이지마다 생성 빈도 감소량

    def __init__(self, window):
        self.window = window
        self.goodiesList = []
        self.nFramesTilNextGoodie = 0

        # 초기 난이도 설정을 위한 변수들 (resetInitialRates에서 활용)
        self.initial_goodie_rate_lo = GoodieMgr.INITIAL_GOODIE_RATE_LO
        self.initial_goodie_rate_hi = GoodieMgr.INITIAL_GOODIE_RATE_HI
        
        self.resetInitialRates() # 초기 설정 적용

    def reset(self): # 게임 리셋 시 호출. Goodie 리스트 초기화.
        self.goodiesList = []
        self.nFramesTilNextGoodie = 0
        self.resetInitialRates() # 난이도 설정을 초기 상태로 되돌림

    def resetInitialRates(self): # 현재 난이도 설정을 초기화 (새로운 난이도 적용 시 호출)
        self.current_goodie_rate_lo = self.initial_goodie_rate_lo
        self.current_goodie_rate_hi = self.initial_goodie_rate_hi

    def setInitialRates(self, rate_lo, rate_hi): # 난이도에 따라 생성 빈도 설정
        self.initial_goodie_rate_lo = rate_lo
        self.initial_goodie_rate_hi = rate_hi
        self.resetInitialRates() # 새 빈도로 재설정

    def update(self, playerRect):
        nGoodiesHit = 0
        goodiesToKeep = [] # 화면에 남길 굿디들을 저장할 리스트

        for oGoodie in self.goodiesList:
            oGoodie.update()
            # 굿디가 화면 밖으로 벗어나면 제거
            if (oGoodie.direction == Goodie.LEFT and oGoodie.x > oGoodie.minLeft) or \
               (oGoodie.direction == Goodie.RIGHT and oGoodie.x < WINDOW_WIDTH):
                goodiesToKeep.append(oGoodie)
            
            # 플레이어와 충돌했으면 점수 증가 및 제거
            if oGoodie.collide(playerRect):
                nGoodiesHit = nGoodiesHit + 1
                # 충돌한 굿디는 리스트에서 제거 (baddiesToKeep에 추가하지 않음)
        
        self.goodiesList = goodiesToKeep # 화면에 남은 굿디들만 다시 리스트에 할당

        # 굿디 생성 주기 관리
        self.nFramesTilNextGoodie = self.nFramesTilNextGoodie - 1
        if self.nFramesTilNextGoodie == 0:
            # 현재 난이도 설정에 따른 빈도로 새로운 굿디 생성
            oGoodie = Goodie(self.window)
            self.goodiesList.append(oGoodie)
            self.nFramesTilNextGoodie = random.randrange(
                                                            self.current_goodie_rate_lo,
                                                            self.current_goodie_rate_hi)

        return nGoodiesHit  # 플레이어가 획득한 굿디 수 반환

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
            self.current_goodie_rate_hi = self.current_goodie_rate_lo