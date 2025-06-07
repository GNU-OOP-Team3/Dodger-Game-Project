# Goodies.py
import pygame
import random
from Constants import * # 모든 상수를 임포트
import time # Goodie 생성 시간 관리를 위해 추가

class Goodie():
    def __init__(self, window, windowWidth, windowHeight, startingX, startingY):
        self.window = window
        self.windowWidth = windowWidth
        self.windowHeight = windowHeight
        self.image = pygame.image.load('images/goodie.png') # goodie 이미지 로드
        self.goodieRect = self.image.get_rect()
        self.goodieRect.left = startingX
        self.goodieRect.top = startingY
        self.speed = random.randint(3, 6) # Goodie는 일정한 속도 범위 유지

    def update(self):
        # Goodie를 아래로 이동시킵니다.
        self.goodieRect.top = self.goodieRect.top + self.speed

    def draw(self):
        self.window.blit(self.image, self.goodieRect)

    def getRect(self):
        return self.goodieRect

class GoodieMgr():
    def __init__(self, window):
        self.window = window
        self.reset() # 초기화 시 reset 호출

    def reset(self):
        # 초기화 시 상수를 사용하여 초기 빈도를 설정
        self.goodies = []
        self.goodieRateLo = GOODIE_INITIAL_RATE_LO
        self.goodieRateHi = GOODIE_INITIAL_RATE_HI
        # 이제 프레임 카운트 대신 pygame.time.get_ticks()를 사용하여 시간 기반으로 Goodie 생성
        self.lastGoodieAddedTime = pygame.time.get_ticks() 
        # self.nGoodiesHit = 0 # Goodie 획득 횟수는 ScenePlay에서 관리하므로 여기서 제거

    def setInitialFrequency(self, frequency_factor):
        # ScenePlayStage의 enter에서 난이도에 따라 초기 Goodie 생성 빈도를 설정합니다.
        # frequency_factor는 1.2 (Easy, 더 자주), 1.0 (Normal), 0.8 (Hard, 덜 자주) 같은 값으로 전달됩니다.
        # 값이 작을수록 더 자주 나타남
        self.goodieRateLo = int(GOODIE_INITIAL_RATE_LO / frequency_factor)
        self.goodieRateHi = int(GOODIE_INITIAL_RATE_HI / frequency_factor)
        
        # 최소값 설정 (너무 자주 나타나지 않도록)
        if self.goodieRateLo < 10: self.goodieRateLo = 10
        if self.goodieRateHi < self.goodieRateLo + 10: self.goodieRateHi = self.goodieRateLo + 10

        print(f"GoodieMgr: Initial Goodie Rate Lo: {self.goodieRateLo}, Hi: {self.goodieRateHi}")

    def update(self, playerRect):
        # Goodie 생성 로직
        # 현재 시간 (밀리초)
        currentTime = pygame.time.get_ticks()
        # 마지막 Goodie 추가 시간과 현재 시간의 차이가 설정된 간격보다 크면 새로운 Goodie 추가
        if currentTime - self.lastGoodieAddedTime > random.randint(self.goodieRateLo, self.goodieRateHi) * 10: # 10을 곱하여 밀리초 단위로 변환
            self._addRandomGoodie()
            self.lastGoodieAddedTime = currentTime

        nGoodiesHitThisFrame = 0
        goodiesToRemove = []
        for oGoodie in self.goodies:
            oGoodie.update()
            if oGoodie.getRect().top > self.window.get_height(): # 화면 아래로 벗어나면
                goodiesToRemove.append(oGoodie)
            elif playerRect.colliderect(oGoodie.getRect()): # 플레이어와 충돌하면
                goodiesToRemove.append(oGoodie)
                nGoodiesHitThisFrame += 1 # 획득 카운트 증가

        for oGoodie in goodiesToRemove:
            self.goodies.remove(oGoodie)
        
        # self.nGoodiesHit += nGoodiesHitThisFrame # 총 획득 횟수 누적은 ScenePlay에서 관리
        return nGoodiesHitThisFrame # 현재 프레임에서 획득한 Goodie 수 반환

    def draw(self):
        # 모든 Goodie를 그립니다.
        for oGoodie in self.goodies:
            oGoodie.draw()

    def _addRandomGoodie(self):
        # 무작위 위치로 Goodie를 생성합니다.
        startingX = random.randint(0, self.window.get_width() - 50) # Goodie 이미지 너비 고려
        startingY = random.randint(-self.window.get_height(), -50) # 화면 위쪽에서 시작
        oGoodie = Goodie(self.window, self.window.get_width(), self.window.get_height(),
                         startingX, startingY)
        self.goodies.append(oGoodie)

    def increaseFrequency(self, stage):
        # 스테이지가 증가할수록 Goodie 생성 빈도를 높여(시간 간격 줄임) 난이도 증가
        # 숫자가 작아질수록 자주 나타납니다.
        # 너무 자주 나타나지 않도록 하한선을 설정합니다.
        if self.goodieRateLo > 20: # 최소 20ms 간격보다는 줄이지 않음
            self.goodieRateLo -= 5
        if self.goodieRateHi > 40: # 최소 40ms 간격보다는 줄이지 않음
            self.goodieRateHi -= 5
        
        print(f"GoodieMgr: Stage {stage} - Goodie Rate Lo: {self.goodieRateLo}, Hi: {self.goodieRateHi}")