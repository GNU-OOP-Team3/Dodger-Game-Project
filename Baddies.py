# Baddies.py
import pygame
import pygwidgets
import random
from Constants import (WINDOW_WIDTH, GAME_HEIGHT, BLACK,
                        BADDIE_MIN_SPEED_BASE, BADDIE_MAX_SPEED_BASE) # 필요한 상수 임포트

class Baddy():
    # Baddy 객체는 속도, 이미지, 위치를 가집니다.
    def __init__(self, window, startX, startY, speed):
        self.window = window
        self.image = pygwidgets.Image(self.window, (startX, startY), 'images/baddy.png') # baddy.png 필요
        self.rect = self.image.getRect()
        self.speed = speed

    def update(self):
        # Baddy를 아래로 이동시킵니다.
        self.rect.move_ip(0, self.speed)
        self.image.setLoc(self.rect.topleft) # 이미지 위치 업데이트

    def draw(self):
        self.image.draw()

    def getRect(self):
        return self.rect

    def isOffScreen(self):
        # Baddy가 화면 아래로 벗어났는지 확인합니다.
        return self.rect.top > GAME_HEIGHT # GAME_HEIGHT보다 아래로 내려가면 화면 밖


class BaddieMgr():
    def __init__(self, window):
        self.window = window
        self.baddies = [] # 현재 활성화된 Baddy 객체들을 저장하는 리스트

    def addBaddy(self, speedMultiplier=1.0): # speedMultiplier 인자 추가
        # 새 Baddy를 생성하고 리스트에 추가합니다.
        # 화면 상단에서 랜덤한 X 위치에 나타납니다.
        # 속도는 상수와 speedMultiplier에 따라 달라집니다.
        minSpeed = int(BADDY_MIN_SPEED_BASE * speedMultiplier)
        maxSpeed = int(BADDY_MAX_SPEED_BASE * speedMultiplier)
        if minSpeed == 0: minSpeed = 1 # 최소 속도가 0이 되는 것을 방지

        speed = random.randint(minSpeed, maxSpeed)
        
        startX = random.randint(0, WINDOW_WIDTH - 50) # Baddy 이미지 너비를 50으로 가정
        startY = random.randint(-100, -50) # 화면 위에서 나타나도록 음수 Y값 사용

        newBaddy = Baddy(self.window, startX, startY, speed)
        self.baddies.append(newBaddy)

    def update(self, playerRect):
        # 각 Baddy를 업데이트하고, 플레이어와의 충돌을 감지합니다.
        # 화면 밖으로 나간 Baddy는 제거하고, 충돌한 Baddy는 제거합니다.
        baddiesHit = 0
        baddiesToRemove = []

        for baddy in self.baddies:
            baddy.update()
            if baddy.isOffScreen():
                baddiesToRemove.append(baddy)
            elif playerRect.colliderect(baddy.getRect()):
                baddiesHit += 1
                baddiesToRemove.append(baddy)

        # 제거할 Baddy들을 리스트에서 실제로 제거합니다.
        for baddy in baddiesToRemove:
            self.baddies.remove(baddy)

        return baddiesHit

    def draw(self):
        # 모든 Baddy들을 그립니다.
        for baddy in self.baddies:
            baddy.draw()

    def reset(self):
        # 모든 Baddy들을 제거하여 초기화합니다.
        self.baddies = []